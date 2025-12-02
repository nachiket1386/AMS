"""
ConflictResolver for handling data conflicts during restore
"""


class ConflictResolver:
    """Service for detecting and resolving conflicts during restore"""
    
    def detect_conflicts(self, backup_record, db_record):
        """
        Check if two records conflict (same key, different data)
        
        Args:
            backup_record: Record dict from backup file
            db_record: Record dict from database
            
        Returns:
            bool: True if records conflict (different data), False if identical
        """
        if not backup_record or not db_record:
            return False
        
        # Compare checksums if available
        backup_checksum = backup_record.get('checksum')
        db_checksum = db_record.get('checksum')
        
        if backup_checksum and db_checksum:
            return backup_checksum != db_checksum
        
        # Fallback to field-by-field comparison
        return self._records_differ(backup_record, db_record)
    
    def apply_merge_strategy(self, backup_record, db_record, strategy='backup_wins'):
        """
        Apply merge strategy to resolve conflict
        
        Args:
            backup_record: Record from backup file
            db_record: Existing database record
            strategy: 'backup_wins', 'database_wins', or 'manual'
            
        Returns:
            dict representing the merged record
        """
        if strategy == 'backup_wins':
            return backup_record
        elif strategy == 'database_wins':
            return db_record
        elif strategy == 'manual':
            # For now, default to backup_wins for manual strategy
            # In a full implementation, this would prompt the user
            return backup_record
        else:
            raise ValueError(f"Unknown merge strategy: {strategy}")
    
    def _records_differ(self, record1, record2):
        """
        Compare two records excluding timestamps and checksums
        
        Args:
            record1: First record dict
            record2: Second record dict
            
        Returns:
            bool: True if records differ, False if identical
        """
        # Fields to exclude from comparison
        exclude_fields = {'checksum', 'created_at', 'updated_at', 'id'}
        
        # Get all keys from both records
        all_keys = set(record1.keys()) | set(record2.keys())
        
        # Compare each field
        for key in all_keys:
            if key in exclude_fields:
                continue
            
            val1 = record1.get(key)
            val2 = record2.get(key)
            
            # Normalize None and empty string
            if val1 in (None, ''):
                val1 = None
            if val2 in (None, ''):
                val2 = None
            
            if val1 != val2:
                return True
        
        return False
