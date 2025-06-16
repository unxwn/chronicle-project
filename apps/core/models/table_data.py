from django.db import models
import json


class TableData(models.Model):
    """Table structure for table-type notes"""
    note = models.OneToOneField(
        'Note',
        on_delete=models.CASCADE,
        related_name='table_data'
    )
    headers = models.JSONField(default=list)  # ['Name', 'Age', 'City']
    rows = models.JSONField(default=list)  # [['John', '25', 'NYC'], ...]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Table Data"
        verbose_name_plural = "Table Data"

    def __str__(self):
        return f"Table for {self.note.title}"

    def add_row(self, row_data):
        """Add a new row to the table"""
        if not isinstance(self.rows, list):
            self.rows = []
        self.rows.append(row_data)
        self.save()

    def add_column(self, header_name, default_value=""):
        """Add a new column to the table"""
        if not isinstance(self.headers, list):
            self.headers = []
        if not isinstance(self.rows, list):
            self.rows = []

        self.headers.append(header_name)
        # Add default value to all existing rows
        for row in self.rows:
            row.append(default_value)
        self.save()

    @property
    def row_count(self):
        return len(self.rows) if self.rows else 0

    @property
    def column_count(self):
        return len(self.headers) if self.headers else 0
