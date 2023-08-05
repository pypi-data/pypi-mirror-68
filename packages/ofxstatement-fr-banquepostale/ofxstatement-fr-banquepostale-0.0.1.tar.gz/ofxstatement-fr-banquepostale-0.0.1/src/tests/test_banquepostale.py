# Copyright 2020 crepi22
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""unit tests for banquepostale ofxstatement plugin"""

from datetime import datetime
from decimal import Decimal
import importlib.resources as pkg_resources
import unittest

from ofxstatement.plugins.fr.banquepostale import (
    BanquePostaleParser, BanquePostaleStateMachine, ParseState, RawStatement
)
# pylint: disable=import-error,no-name-in-module
from ofxstatement.exceptions import ParseError
from ofxstatement.statement import Statement

from . import resources


class BanquePostaleStateMachineTest(unittest.TestCase):
    "Unit tests for the parser's state machine"

    def setUp(self):
        self.statement = Statement()
        self.machine = (
            BanquePostaleStateMachine(self.statement))

    def test_prelude_state_header(self):
        "Case header line found in prelude state"
        line = (
            "Date      Opérations                                         "
            "                                    Débit (¤)         "
            "Crédit (¤)")
        self.machine.state_prelude(line)
        self.assertIs(
            self.machine.state, ParseState.HEADER,
            "Changed state to Header")
        self.assertEqual(self.machine.pos_deb, line.index("Débit"))
        self.assertEqual(self.machine.pos_cred, line.index("Crédit"))

    def test_prelude_state_iban(self):
        "Case iban line found in prelude state"
        # 0: ? 1: bank_id 2: branch_id 3: account_id 4: key
        # no support for branch_id or key in ofxstatement
        line = "IBAN : FR00 1111 1222 2233 3333 3A33 344 | BIC : AAAAAAAAAA"
        self.machine.state_prelude(line)
        self.assertEqual(self.statement.bank_id, "11111")
        self.assertEqual(self.statement.account_id, "3333333A333")
        self.assertEqual(self.machine.state, ParseState.PRELUDE)

    def test_prelude_state_other(self):
        "Case other lines in prelude state"
        line = "Whatever your bank has to say"
        self.machine.state_prelude(line)
        self.assertEqual(self.machine.state, ParseState.PRELUDE)

    def init_header_state(self):
        "Initialize machine for header state"
        self.machine.state = ParseState.HEADER

    def test_header_state_balance(self):
        "case where old balance is found"
        line = (
            "                                                           "
            "Ancien solde au 01/02/1999                           1 234,56")
        self.init_header_state()
        self.machine.state_header(line)
        self.assertIs(self.machine.state, ParseState.STATEMENT)
        start_date = self.statement.start_date
        self.assertEqual(start_date.year, 1999)
        self.assertEqual(start_date.month, 2)
        self.assertEqual(start_date.day, 1)
        self.assertEqual(self.statement.start_balance, Decimal('1234.56'))

    def test_header_state_other(self):
        "Case not the balance (usually empty line)"
        line = ""
        self.init_header_state()
        self.machine.state_header(line)
        self.assertIs(self.machine.state, ParseState.HEADER)

    def init_statement_state(self):
        "Initialize machine for statement state"
        self.machine.state = ParseState.STATEMENT
        self.machine.pos_deb = 99
        self.machine.pos_cred = 115
        self.machine.partial_credit = Decimal("70000.00")
        self.machine.partial_debit = Decimal("80000.00")

    def test_statement_state_main_line_credit(self):
        "Parsing of a credit line"
        line = (
            "12/03    VIREMENT DE XXXX PAIE CCP                "
            "                                                  "
            "                                 1 234,56")
        self.init_statement_state()
        next(self.machine.state_statement(line), None)
        result = self.machine.current_stmt_line
        self.assertEqual(result.date, "12/03")
        self.assertEqual(result.memo, [])
        self.assertEqual(result.payee, "VIREMENT DE XXXX PAIE CCP")
        self.assertEqual(result.amount, Decimal("1234.56"))
        self.assertEqual(self.machine.partial_credit, Decimal("71234.56"))
        self.assertEqual(self.machine.partial_debit, Decimal("80000"))
        self.assertIs(self.machine.state, ParseState.STATEMENT)
        # We pop the previous run
        elem = [x for x in self.machine.state_statement(line)]
        self.assertEqual(elem, [result])

    def test_statement_state_main_line_debit(self):
        "Parsing of a debit line"
        line = (
            "03/04 PRELEVEMENT DE xxxx                                        "
            "                                   1,23")
        self.init_statement_state()
        next(self.machine.state_statement(line), None)
        result = self.machine.current_stmt_line
        self.assertEqual(result.date, "03/04")
        self.assertEqual(result.payee, "PRELEVEMENT DE xxxx")
        self.assertEqual(result.amount, Decimal("-1.23"))
        self.assertEqual(self.machine.partial_credit, Decimal("70000"))
        self.assertEqual(self.machine.partial_debit, Decimal("80001.23"))


    def test_statement_state_additional_line(self):
        "Parsing of continuation lines"
        line1 = (
            "03/04 PRELEVEMENT DE xxxx                                        "
            "                                   1,23")
        line2 = "          CARTE NUMERO 000"
        line3 = "          CARTE NUMERO 111"
        line4 = ""
        self.init_statement_state()
        for line in [line1, line2, line3, line4]:
            next(self.machine.state_statement(line), None)
        result = self.machine.current_stmt_line
        self.assertEqual(result.memo, [line2.strip(), line3.strip()])

    def test_statement_state_header(self):
        "Case header renewed in statement state"
        line = (
            "  Date      Opérations                                         "
            "                                    Débit (¤)         "
            "Crédit (¤)")
        self.init_statement_state()
        next(self.machine.state_statement(line), None)
        self.assertIs(self.machine.state, ParseState.STATEMENT)
        self.assertEqual(self.machine.pos_deb, line.index("Débit"))
        self.assertEqual(self.machine.pos_cred, line.index("Crédit"))

    def test_statement_state_total(self):
        "Case totals found in statement state"
        line = (
            "                                                                "
            "           Total des opérations               80 000,00         "
            "     70 000,00")
        self.init_statement_state()
        next(self.machine.state_statement(line), None)
        self.assertIs(self.machine.state, ParseState.FOOTER)
        # incorrect debit
        line1 = line.replace("8", "9")
        self.assertRaises(
            ParseError,
            lambda t: next(self.machine.state_statement(line1), None),
            ())
        # incorrect credit
        line2 = line.replace("7", "9")
        self.assertRaises(
            ParseError,
            lambda t: next(self.machine.state_statement(line2), None),
            ())

    def test_statement_state_other(self):
        "Case other lines in statement state"
        line1 = (
            "03/04 PRELEVEMENT DE xxxx                                        "
            "                                   1,23")
        self.init_statement_state()
        next(self.machine.state_statement(line1), None)
        stmt_line = self.machine.current_stmt_line
        lines = [
            "Page 1/2"
            "^L   "
            "        Relevé n° 1 | 01/01/2020"
            " "
            "          MR DUPONT DUPOND"
        ]
        for line in lines:
            next(self.machine.state_statement(line), None)
            self.assertEqual(self.machine.current_stmt_line, stmt_line)
            self.assertIs(self.machine.state, ParseState.STATEMENT)

    def init_footer_state(self):
        "Initialize machine for footer state"
        self.machine.state = ParseState.FOOTER
        self.statement.start_balance = Decimal("30000.00")
        self.machine.partial_credit = Decimal("70000.00")
        self.machine.partial_debit = Decimal("80000.00")

    def test_footer_state_balance(self):
        "Case balance found in footer state"
        line = (
            "                                                              "
            "Nouveau solde au 01/05/2020                                   "
            "       20 000,00")
        self.init_footer_state()
        self.machine.state_footer(line)
        self.assertEqual(self.statement.end_balance, Decimal("20000.00"))
        self.assertEqual(
            self.statement.end_date,
            datetime(year=2020, month=5, day=1))
        self.assertIs(self.machine.state, ParseState.POSTLUDE)

    # We must reinit. Cannot reuse previous test (state changed)
    def test_footer_state_bad_balance(self):
        "Case balance found in footer state"
        line = (
            "                                                              "
            "Nouveau solde au 01/05/2020                                   "
            "       20 001,00")
        self.init_footer_state()
        self.assertRaises(
            ParseError,
            lambda t: self.machine.state_footer(line),
            ())

    def test_footer_state_other(self):
        "Case balance found in footer state"
        self.init_footer_state()
        line = ""
        self.machine.state_footer(line)
        self.assertIs(self.machine.state, ParseState.FOOTER)

def rstmt(payee, memo):
    'simple raw statement'
    return RawStatement(
        date="01/01", payee=payee, memo=memo, amount=Decimal(10.00)
    )

class BanquePostaleParserTest(unittest.TestCase):
    "Tests at the level of the parser"

    def setUp(self):
        self.parser = BanquePostaleParser("foo", {})
        self.parser.statement.start_date = datetime(year=2019, month=11, day=20)

    def test_split_records_ok(self):
        "Parsing of a complete statement"
        self.parser.input = pkg_resources.open_text(
            resources, "releve.txt", encoding="utf-8")
        raw_stmts = [stmt for stmt in self.parser.split_records()]
        self.assertEqual(len(raw_stmts), 3)
        self.assertTrue(all(isinstance(x, RawStatement) for x in raw_stmts))

    def test_split_records_truncated(self):
        "Parsing of a truncated statement"
        self.parser.input = pkg_resources.open_text(
            resources, "bad_releve.txt", encoding="utf-8")
        self.assertRaises(
            ParseError,
            lambda x: [stmt for stmt in self.parser.split_records()],
            ())

    def test_parse_record_date_simple(self):
        "Check correct parsing of date"
        raw = RawStatement(
            date="11/12",
            payee="AAAAA AAAAA",
            memo=["BBBB BBBB", "CCCC CCCC"],
            amount=Decimal(10.00)
        )
        output = self.parser.parse_record(raw)
        self.assertEqual(output.date, datetime(year=2019, month=12, day=11))
        self.assertEqual(output.trntype, "OTHER")
        self.assertEqual(output.payee, "AAAAA AAAAA")
        self.assertEqual(output.memo, "BBBB BBBB CCCC CCCC")

    def test_parse_record_date_enhanced(self):
        "Check date when year change"
        raw = RawStatement(
            date="05/02",
            payee="AAAAA AAAAA",
            memo=["BBBB BBBB", "CCCC CCCC"],
            amount=Decimal(10.00)
        )
        output = self.parser.parse_record(raw)
        self.assertEqual(output.date, datetime(year=2020, month=2, day=5))

    def test_parse_record_prelevement(self):
        "Check payment"
        raw = rstmt(
            "PRELEVEMENT DE AAAAAAAAA BBBBBBB CCCCC",
            ["CCCC DDD REF : AAA---000000000000000000000000000000000000 00"])
        output = self.parser.parse_record(raw)
        self.assertEqual(
            output.payee,
            "PRELEVEMENT DE AAAAAAAAA BBBBBBB CCCCCCCCC DDD")
        self.assertEqual(
            output.memo,
            "REF : AAA---000000000000000000000000000000000000 00")
        self.assertEqual(output.trntype, "PAYMENT")

    def test_parse_record_achat_cb(self):
        "Check Point of sale"
        raw = rstmt(
            "ACHAT CB FOO BAR INC 01.01.20",
            ["CARTE NUMERO 123"]
        )
        output = self.parser.parse_record(raw)
        self.assertEqual(output.trntype, "POS")

    def test_parse_record_cheque(self):
        "Check cheque"
        raw = rstmt(
            "CHEQUE N° 1234567",
            ["CARTE NUMERO 123"]
        )
        output = self.parser.parse_record(raw)
        self.assertEqual(output.trntype, "CHECK")
        self.assertEqual(output.check_no, "1234567")
        raw = rstmt(
            "REMISE DE CHEQUE N° 1234567",
            ["DE M FOO BAR"]
        )
        output = self.parser.parse_record(raw)
        self.assertEqual(output.trntype, "CHECK")
        self.assertEqual(output.check_no, "1234567")


    def test_parse_record_virement(self):
        "Check directdep"
        raw = rstmt(
            "VIREMENT DE FOO BAR",
            ["INC REF : 000000"]
        )
        output = self.parser.parse_record(raw)
        self.assertEqual(output.trntype, "DIRECTDEP")
        self.assertEqual(output.payee, "VIREMENT DE FOO BARINC")

    def test_parse_record_retrait(self):
        "Check ATM"
        raw = rstmt(
            "CARTE X0000 01/01/20 A 12H00",
            ["RETRAIT DAB ICI OU LA"])
        output = self.parser.parse_record(raw)
        self.assertEqual(output.trntype, "ATM")
        raw = rstmt(
            "RETRAIT CASH WITHDRAWAL 01.01.20",
            ["EUR 100,00 CARTE NO 000"])
        output = self.parser.parse_record(raw)
        self.assertEqual(output.trntype, "ATM")

    def test_parse_record_credit(self):
        "Check credit"
        raw = rstmt(
            "CREDIT CARTE BANCAIRE",
            ["FOOBAR 01.01.20 CARTE NUMERO 000"])
        output = self.parser.parse_record(raw)
        self.assertEqual(output.trntype, "CREDIT")

    def test_parse_record_cotisation(self):
        "Check debit"
        raw = rstmt(
            "COTISATION TRIMESTRIELLE",
            ["COMPTE XXXXX YYYYY"]
        )
        output = self.parser.parse_record(raw)
        self.assertEqual(output.trntype, "DEBIT")

