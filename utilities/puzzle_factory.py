# Importa tus clases de puzzle aquí cuando las crees
# from game_objects.puzzles.statue_puzzle import StatuePuzzle

class PuzzleFactory:
    @staticmethod
    def create_puzzle(puzzle_data):
        puzzle_type = puzzle_data.get("type")
        
        if puzzle_type == "StatuePuzzle":
            print("Fábrica: Creando Puzzle de Estatuas")
            # return StatuePuzzle(puzzle_data)
            return None # Placeholder hasta que crees la clase
            
        elif puzzle_type == "SoundPuzzle":
            print("Fábrica: Creando Puzzle de Sonido")
            # return SoundPuzzle(puzzle_data)
            return None
            
        else:
            print(f"Error: Tipo de puzzle desconocido '{puzzle_type}'")
            return None