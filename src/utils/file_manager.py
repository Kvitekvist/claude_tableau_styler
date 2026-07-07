"""
File Manager

Handles safe file I/O operations for Tableau workbooks.
Creates backups, writes styled outputs, manages .twb and .twbx formats.
"""

import os
import shutil
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
from lxml import etree

from parser.workbook import Workbook


class FileManagerError(Exception):
    """Base exception for file manager errors"""
    pass


class BackupFailedError(FileManagerError):
    """Failed to create backup"""
    pass


class WriteFailedError(FileManagerError):
    """Failed to write output file"""
    pass


class FileManager:
    """Manages file operations for Tableau workbooks"""

    def __init__(self):
        self.temp_dir = None

    def create_backup(self, original_path: str, backup_dir: str = "tableau/backups") -> str:
        """
        Create a timestamped backup of the original file

        Args:
            original_path: Path to original file
            backup_dir: Directory to store backups

        Returns:
            Path to backup file

        Raises:
            BackupFailedError: If backup creation fails
        """
        try:
            # Create backup directory if it doesn't exist
            os.makedirs(backup_dir, exist_ok=True)

            # Generate timestamped backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = Path(original_path).stem
            extension = Path(original_path).suffix
            backup_filename = f"{filename}_backup_{timestamp}{extension}"
            backup_path = os.path.join(backup_dir, backup_filename)

            # Copy file
            shutil.copy2(original_path, backup_path)

            # Verify backup was created
            if not os.path.exists(backup_path):
                raise BackupFailedError(f"Backup file not created: {backup_path}")

            return backup_path

        except Exception as e:
            raise BackupFailedError(f"Failed to create backup: {e}") from e

    def write(
        self,
        workbook: Workbook,
        original_path: str,
        output_dir: str = "tableau/output"
    ) -> str:
        """
        Write styled workbook to output file

        Args:
            workbook: Styled workbook to write
            original_path: Original file path (for naming)
            output_dir: Directory to write output

        Returns:
            Path to output file

        Raises:
            WriteFailedError: If write operation fails
        """
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)

            # Generate output filename
            output_path = self._generate_output_path(original_path, output_dir)

            # Write based on file type
            if workbook.file_type == 'twbx':
                self._write_twbx(workbook, output_path)
            else:
                self._write_twb(workbook, output_path)

            # Verify output was created
            if not os.path.exists(output_path):
                raise WriteFailedError(f"Output file not created: {output_path}")

            return output_path

        except Exception as e:
            raise WriteFailedError(f"Failed to write output: {e}") from e

    def _generate_output_path(self, original_path: str, output_dir: str) -> str:
        """
        Generate output file path with _styled suffix

        Args:
            original_path: Original file path
            output_dir: Output directory

        Returns:
            Output file path
        """
        filename = Path(original_path).stem
        extension = Path(original_path).suffix
        output_filename = f"{filename}_styled{extension}"
        output_path = os.path.join(output_dir, output_filename)

        # Handle filename collisions
        counter = 1
        while os.path.exists(output_path):
            output_filename = f"{filename}_styled_{counter}{extension}"
            output_path = os.path.join(output_dir, output_filename)
            counter += 1

        return output_path

    def _write_twb(self, workbook: Workbook, output_path: str) -> None:
        """
        Write .twb file (uncompressed XML)

        Args:
            workbook: Workbook to write
            output_path: Output file path
        """
        # Write to temporary file first for safety
        temp_path = output_path + ".tmp"

        try:
            # CRITICAL: Use xml_root, not xml_tree!
            # xml_tree may not reflect modifications made to xml_root
            # Rebuild the tree from the modified root
            tree = etree.ElementTree(workbook.xml_root)
            tree.write(
                temp_path,
                encoding='utf-8',
                xml_declaration=True,
                pretty_print=True
            )

            # Move to final location
            shutil.move(temp_path, output_path)

        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise

    def _write_twbx(self, workbook: Workbook, output_path: str) -> None:
        """
        Write .twbx file (compressed ZIP)

        Args:
            workbook: Workbook to write
            output_path: Output file path
        """
        # Create temporary directory for building zip
        self.temp_dir = tempfile.mkdtemp(prefix='tableau_writer_')

        try:
            # Write .twb XML file to temp directory
            twb_filename = Path(workbook.file_path).stem + ".twb"
            twb_path = os.path.join(self.temp_dir, twb_filename)

            # CRITICAL: Rebuild tree from modified root
            tree = etree.ElementTree(workbook.xml_root)
            tree.write(
                twb_path,
                encoding='utf-8',
                xml_declaration=True,
                pretty_print=True
            )

            # Write other zip contents (images, data extracts) if they exist
            if workbook.zip_contents:
                for rel_path, content in workbook.zip_contents.items():
                    # Create subdirectories as needed
                    full_path = os.path.join(self.temp_dir, rel_path)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)

                    # Write content
                    with open(full_path, 'wb') as f:
                        f.write(content)

            # Create ZIP archive
            temp_zip = output_path + ".tmp"
            with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                # Walk temp directory and add all files
                for root, dirs, files in os.walk(self.temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, self.temp_dir)
                        zf.write(file_path, arcname)

            # Move to final location
            shutil.move(temp_zip, output_path)

        finally:
            # Clean up temp directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.temp_dir = None
