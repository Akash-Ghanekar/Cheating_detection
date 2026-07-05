# validate_config.py
import yaml
import os

def validate_config(config_path):
    """Validate your YAML config file"""
    
    print("🔍 Validating config file...")
    
    # Check if file exists
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        return False
    
    # Load and validate YAML syntax
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        print("✅ YAML syntax is valid")
    except Exception as e:
        print(f"❌ YAML syntax error: {e}")
        return False
    
    # Check required fields
    required_fields = ['path', 'train', 'val', 'nc', 'names']
    for field in required_fields:
        if field not in config:
            print(f"❌ Missing required field: {field}")
            return False
    print("✅ All required fields present")
    
    # Check if path exists
    if not os.path.exists(config['path']):
        print(f"❌ Path does not exist: {config['path']}")
        return False
    print(f"✅ Path exists: {config['path']}")
    
    # Check train and val directories
    train_path = os.path.join(config['path'], config['train'])
    val_path = os.path.join(config['path'], config['val'])
    
    if not os.path.exists(train_path):
        print(f"❌ Train directory not found: {train_path}")
        return False
    print(f"✅ Train directory exists: {train_path}")
    
    if not os.path.exists(val_path):
        print(f"❌ Validation directory not found: {val_path}")
        return False
    print(f"✅ Validation directory exists: {val_path}")
    
    # Check if there are images in train/val
    train_images = [f for f in os.listdir(train_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
    val_images = [f for f in os.listdir(val_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    print(f"📊 Training images: {len(train_images)}")
    print(f"📊 Validation images: {len(val_images)}")
    
    if len(train_images) == 0:
        print("❌ No images found in train directory")
        return False
    
    if len(val_images) == 0:
        print("❌ No images found in validation directory")
        return False
    
    # Check class configuration
    if not isinstance(config['nc'], int) or config['nc'] <= 0:
        print(f"❌ nc must be a positive integer, got: {config['nc']}")
        return False
    print(f"✅ Number of classes: {config['nc']}")
    
    if len(config['names']) != config['nc']:
        print(f"❌ Number of class names ({len(config['names'])}) doesn't match nc ({config['nc']})")
        return False
    print(f"✅ Class names: {config['names']}")
    
    print("\n🎉 Config file is VALID! Ready for training.")
    return True

# Run validation
if __name__ == "__main__":
    config_path = r"C:\Users\ghane\Desktop\Detection_project\code\data\config.yaml"
    validate_config(config_path)