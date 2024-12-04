-- NAME OF DATABASE: EncryptedSecuritySystem

CREATE TABLE file_metadata (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY, 
    file_name VARCHAR(255) NOT NULL, 
    encryption_key TEXT NOT NULL,  
    encryption_method VARCHAR(50) NOT NULL, 
    file_path TEXT NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
