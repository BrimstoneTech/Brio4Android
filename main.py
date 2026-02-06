import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.pet_window import PetWindow
from characters.child_robot import ChildRobot
from characters.young_adult_robot import YoungAdultRobot
from characters.elder_robot import ElderRobot

# Map character keys to (Class, AssetPath)
CHARACTER_MAP = {
    'child': (ChildRobot, 'assets/child/child-removebg-preview.png'),
    'young_adult': (YoungAdultRobot, 'assets/young_adult/youth-removebg-preview.png'),
    'elder': (ElderRobot, 'assets/elder/elder-removebg-preview.png'),
}

def main():
    parser = argparse.ArgumentParser(description='Brio Visual Engine')
    parser.add_argument(
        'character',
        choices=['child', 'young_adult', 'elder'],
        default='young_adult',
        nargs='?',
        help='Which character to spawn'
    )
    
    args = parser.parse_args()
    
    if args.character not in CHARACTER_MAP:
        print(f"Unknown character: {args.character}")
        return
        
    char_class, asset_path = CHARACTER_MAP[args.character]
    
    print(f"Starting Brio Visuals: {args.character.upper()}")
    print(f"Loading asset: {asset_path}")
    print("Press ESC in the window to exit.")
    
    app = PetWindow(char_class, asset_path)
    app.initialize()
    app.run()

if __name__ == '__main__':
    main()
