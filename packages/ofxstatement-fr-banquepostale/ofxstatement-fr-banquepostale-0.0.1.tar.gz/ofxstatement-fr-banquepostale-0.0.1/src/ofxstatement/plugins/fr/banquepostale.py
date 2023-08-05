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

"""Ofxstatement plugin for french bank 'La banque Postale'."""
from collections import namedtuple
import datetime
from decimal import Decimal
from enum import Enum
import re
import subprocess

# namespace modules at least of this kind are not understood by pylint.
# pylint: disable=import-error,no-name-in-module
from ofxstatement.exceptions import ParseError
from ofxstatement.plugin import Plugin
from ofxstatement.parser import StatementParser
from ofxstatement.statement import (StatementLine, Statement, generate_transaction_id)


RawStatement = namedtuple("RawStatement", ["date", "payee", "memo", "amount"])


def smart_descr(stmt):
    """Tries to extend description to second line if a REF is mentionned.

    PAYMENT description often span over two lines and the REF is really
    the true separator between description and memo.
    """
    if len(stmt.memo) > 0:
        memo0 = stmt.memo[0]
        try:
            idx = memo0.index(" REF :")
            return RawStatement(
                date=stmt.date,
                payee=stmt.payee + memo0[:idx],
                memo=[memo0[idx+1:]] + stmt.memo[1:],
                amount=stmt.amount
            )
        except ValueError:
            return stmt
    return stmt


TRANSLATIONS = [
    ("PRELEVEMENT ", "PAYMENT", True),
    ("ACHAT CB ", "POS", False),
    ("CHEQUE ", "CHECK", False),
    ("REMISE DE CHEQUE ", "CHECK", False),
    ("CARTE ", "ATM", False),
    ("VIREMENT ", "DIRECTDEP", True),
    ("RETRAIT ", "ATM", False),           # cash withdrawal abroad. Use CASH ?
    ("CREDIT ", "CREDIT", False),
    ("COTISATION ", "DEBIT", False)       # nice wording for banking fee
]


RE_NUMBER = r"\d{1,3}(?: \d{3})*,\d\d"

re_number = re.compile(RE_NUMBER)
re_header = re.compile(
    r"([ ]*Date[ ]{2,})(Opérations[ ]{2,})(Débit \(.\)[ ]{2,})(Crédit \(.\))")
re_old_balance = re.compile(
    r"[ ]{4,}Ancien solde au (\d{2}/\d{2}/\d{4})[ ]{2,}(" + RE_NUMBER + r")")
re_iban = re.compile(
    r"[ ]*IBAN : ((?:[0-9A-Z]{4} ){6}[0-9A-Z]{3}) | BIC : [A-Z0-9]+")
re_statement_line = re.compile(
    r"[ ]*(\d{2}/\d{2}) +((?:[^ ] ?)*[^ ]) {2,}(" + RE_NUMBER + r")")
re_statement_followup = re.compile(r" {5,15}([^ ].*)$")
re_total = re.compile(
    r" {4,}Total des opérations {2,}(" + RE_NUMBER + r") {2,}(" +
    RE_NUMBER + r")")
re_new_balance = re.compile(
    r"[ ]{4,}Nouveau solde au (\d{2}/\d{2}/\d{4})[ ]{2,}(" + RE_NUMBER + r")")
re_check = re.compile(r".*CHEQUE {1,3}N°? {1,2}(\d+) *$")

class ParseState(Enum):
    """ States for banque postale parser"""
    PRELUDE = 1
    HEADER = 2
    STATEMENT = 3
    FOOTER = 4
    POSTLUDE = 5


def parse_decimal(value):
    "parse a decimal value. No reason to make a method out of it"
    return Decimal(value.replace(",", ".").replace(" ", ""))


class BanquePostalePlugin(Plugin):
    """Plugin for La Banque Postale (France) - ofxstatement
    """
    # seriously in a specialized class ?
    #pylint: disable=too-few-public-methods

    def get_parser(self, filename):
        "Get the parser."
        return BanquePostaleParser(filename, self.settings)


class BanquePostaleStateMachine:
    "State machine for the parser"
    def __init__(self, statement):
        self.state = ParseState.PRELUDE
        self.statement = statement
        self.current_stmt_line = None
        self.partial_credit = 0
        self.partial_debit = 0
        self.pos_deb = 0
        self.pos_cred = 0

    def state_prelude(self, line):
        "parse from start of file to column headers"
        match = re_header.match(line)
        if match:
            pos = [len(match.group(i)) for i in range(1, 4)]
            self.pos_deb = pos[0] + pos[1]
            self.pos_cred = self.pos_deb + pos[2]
            self.state = ParseState.HEADER
            return
        match = re_iban.match(line)
        if match:
            iban = match.group(1).replace(' ', '')
            self.statement.bank_id = iban[4:9]
            self.statement.account_id = iban[14:25]
            self.statement.currency = "EUR"

    def state_header(self, line):
        "Parse between column headers and old balance"
        match = re_old_balance.match(line)
        if match:
            start_date = datetime.datetime.strptime(
                match.group(1), "%d/%m/%Y")
            old_balance = parse_decimal(match.group(2))
            self.statement.start_balance = old_balance
            self.statement.start_date = start_date
            self.state = ParseState.STATEMENT

    def state_statement(self, line):
        "core of the parser, yields result"
        match = re_statement_line.match(line)
        if match:
            if self.current_stmt_line is not None:
                yield self.current_stmt_line
            right_pos = len(line)
            if right_pos < self.pos_deb:
                return  # not a well formatted value. Strange line
            amount = parse_decimal(match.group(3))
            if right_pos < self.pos_cred:
                self.partial_debit = self.partial_debit + amount
                amount = - amount
            else:
                self.partial_credit = self.partial_credit + amount
            self.current_stmt_line = RawStatement(
                date=match.group(1),
                payee=match.group(2),
                memo=[],
                amount=amount)
            return
        match = re_statement_followup.match(line)
        if match and self.current_stmt_line is not None:
            self.current_stmt_line.memo.append(match.group(1))
            return
        match = re_header.match(line)
        if match:
            # Positions are not the same on each page. As in state
            # prelude but without state change.
            pos = [len(match.group(i)) for i in range(1, 4)]
            self.pos_deb = pos[0] + pos[1]
            self.pos_cred = self.pos_deb + pos[2]
            return
        match = re_total.match(line)
        if match:
            if self.current_stmt_line:
                yield self.current_stmt_line
            total_debit = parse_decimal(match.group(1))
            total_credit = parse_decimal(match.group(2))
            if self.partial_credit != total_credit:
                raise ParseError(
                    -1,
                    "Computed credit %d != parsed credit %d" % (
                        self.partial_credit, total_credit))
            if self.partial_debit != total_debit:
                raise ParseError(
                    -1,
                    "Computed debit %d != parse debit %d" % (
                        self.partial_debit, total_debit))
            self.state = ParseState.FOOTER

    def state_footer(self, line):
        "parse after totals and until new balance"
        match = re_new_balance.match(line)
        if match:
            end_date = datetime.datetime.strptime(
                match.group(1), "%d/%m/%Y")
            new_balance = parse_decimal(match.group(2))
            computed_balance = (
                self.statement.start_balance +
                self.partial_credit - self.partial_debit)
            if computed_balance != new_balance:
                raise ParseError(
                    -1,
                    "Computed balance %d != parsed balance %d" % (
                        computed_balance, new_balance))
            self.statement.end_balance = new_balance
            self.statement.end_date = end_date
            self.state = ParseState.POSTLUDE


class BanquePostaleParser(StatementParser):
    """Parser for Banque Postale statements in PDF format or text format.

    The parser will use the header to distinguish PDF from regular text files.
    """

    def __init__(self, filename, settings):
        super().__init__()
        self.settings = settings
        self.smart_activated = (
            settings.get("smart", "y") in ["y", "Y", "o", "O"])
        self.filename = filename
        # Missing in 0.6.4
        self.statement = Statement()
        self.input = None

    def parse(self):
        """Main entry point for parsers

        super() implementation will call to split_records and parse_record to
        process the file.
        """
        with open(self.filename, "rb") as fib:
            header = fib.read(5)
        if header == b"%PDF-":
            command = [
                self.settings.get("pdftotext", "pdftotext"),
                "-enc", "UTF-8", "-layout", self.filename, "-"]
            with subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE, encoding="utf-8") as proc:
                self.input = proc.stdout
                return super(BanquePostaleParser, self).parse()
        else:
            # Let us open pre-processed text file. May be useful for debug
            # and manual correction of errors.
            with open(self.filename, "r", encoding="utf-8") as fio:
                self.input = fio
                return super(BanquePostaleParser, self).parse()

    def split_records(self):
        """Return iterable object consisting of a line per transaction

        This version uses a generator approach.
        """
        machine = BanquePostaleStateMachine(self.statement)

        while True:
            line = self.input.readline()
            if not line:
                raise ParseError(
                    -1, "Unexpected end of file while in state %s" % machine.state)
            if machine.state == ParseState.PRELUDE:
                machine.state_prelude(line)
            elif machine.state == ParseState.HEADER:
                machine.state_header(line)
            elif machine.state == ParseState.STATEMENT:
                yield from machine.state_statement(line)
            elif machine.state == ParseState.FOOTER:
                machine.state_footer(line)
            else:
                break

    def parse_record(self, line):
        """Parse given transaction line and return StatementLine object
        """
        short_date = datetime.datetime.strptime(line.date, "%d/%m")
        start_date = self.statement.start_date
        year = (
            start_date.year + 1 if short_date.month < start_date.month
            else start_date.year)
        trans_date = short_date.replace(year=year)
        payee = line.payee
        operation = "OTHER"
        for (prefix, code, smart) in TRANSLATIONS:
            if payee.startswith(prefix):
                operation = code
                if smart and self.smart_activated:
                    line = smart_descr(line)
                break
        stmt_line = StatementLine(
            date=trans_date,
            memo=" ".join(line.memo),
            amount=line.amount)
        if operation == "CHECK":
            match = re_check.match(line.payee)
            if match:
                stmt_line.check_no = match.group(1)
        stmt_line.payee = line.payee
        stmt_line.trntype = operation
        stmt_line.id = generate_transaction_id(stmt_line)
        return stmt_line
