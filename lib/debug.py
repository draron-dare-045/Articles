from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database

def debug():
    print("Starting debug session...")
    print("Available classes: Author, Magazine, Article")
    print("Try things like: Author.get_all(), Magazine.find_by_category('Technology'), etc.")
    print("Type 'exit' to quit")
    
    while True:
        try:
            command = input(">>> ")
            if command.lower() == 'exit':
                break
            if command.lower() == 'seed':
                seed_database()
                print("Database reseeded!")
                continue
            try:
                result = eval(command)
                if result is not None:
                    print(result)
            except Exception as e:
                print(f"Error: {e}")
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    debug()