import json
import argparse
import os
from datetime import datetime
import sys
from typing import Any

class JSONPrettyPrinter:
    def __init__(self):
        self.parser = self.create_parser()
        self.args = self.parser.parse_args()
        self.input_data = self.get_input_data()

    def create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description='JSON Pretty Printer with Smart Features',
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument(
            '-i', '--indent',
            type=int,
            default=4,
            help='Indentation level (default: 4)'
        )
        parser.add_argument(
            '-o', '--output',
            type=str,
            help='Output file name (default: timestamp-based)'
        )
        parser.add_argument(
            '-s', '--sort-keys',
            action='store_true',
            help='Sort JSON keys alphabetically'
        )
        parser.add_argument(
            '-c', '--compact',
            action='store_true',
            help='Compact mode (minify JSON)'
        )
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Show verbose output'
        )
        return parser

    def get_input_data(self) -> str:
        """Improved multi-line input with empty line termination"""
        print("Paste your JSON data (press Enter twice to finish):")
        print("(Or type 'END' on a new line to finish)\n")
        
        lines = []
        try:
            while True:
                line = input()
                if line.lower() == 'end':
                    break
                if not line.strip():  # Check for empty line
                    if len(lines) > 0:  # Only break if we have content
                        break
                    continue
                lines.append(line)
        except EOFError:
            pass
        
        return '\n'.join(lines)

    def validate_and_parse(self) -> Any:
        """Smart JSON parsing with error handling"""
        try:
            return json.loads(self.input_data)
        except json.JSONDecodeError as e:
            print(f"\nInvalid JSON: {e}")
            print(f"Error at line {e.lineno}, column {e.colno}")  # Fixed from colpos to colno
            print(f"Problematic text: {e.doc[e.pos-20:e.pos+20]}...")  # Show more context
            print("Common fixes:")
            print("- Check for missing commas or brackets")
            print("- Remove trailing commas")
            print("- Ensure only one JSON object exists")
            sys.exit(1)
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            sys.exit(1)

    def generate_filename(self) -> str:
        """Smart filename generation"""
        if self.args.output:
            return self.args.output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"pretty_json_{timestamp}.json"

    def handle_existing_file(self, filename: str) -> bool:
        """Smart file conflict resolution"""
        if os.path.exists(filename):
            response = input(f"File '{filename}' exists. Overwrite? [y/N] ").lower()
            return response == 'y'
        return True

    def format_json(self, data: Any) -> str:
        """Smart formatting based on arguments"""
        if self.args.compact:
            return json.dumps(data, separators=(',', ':'))
        
        return json.dumps(
            data,
            indent=self.args.indent,
            sort_keys=self.args.sort_keys,
            ensure_ascii=False
        )

    def run(self):
        """Main execution flow"""
        if not self.input_data:
            print("No input received!")
            return

        data = self.validate_and_parse()
        formatted_json = self.format_json(data)
        
        if self.args.verbose:
            print("\nFormatted JSON:")
            print(formatted_json)

        filename = self.generate_filename()
        
        if self.handle_existing_file(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(formatted_json)
            print(f"\nJSON successfully saved to: {os.path.abspath(filename)}")
        else:
            print("Operation cancelled.")

if __name__ == "__main__":
    try:
        processor = JSONPrettyPrinter()
        processor.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)