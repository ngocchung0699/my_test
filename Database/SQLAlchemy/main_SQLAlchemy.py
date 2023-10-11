from importlib import resources
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append("Database/SQLAlchemy")
from BookRepository import get_books_by_publishers, get_authors_by_publishers, get_authors, add_new_book, output_author_hierarchy
from Models import Base

def main():
    """Main entry point of program"""
    # Connect to the database using SQLAlchemy
    # with resources.path(
    #     "Database/SQLAlchemy", "author_book_publisher.db"
    # ) as sqlite_filepath:
    #     engine = create_engine(f"sqlite:///{sqlite_filepath}")

    engine = create_engine('sqlite:///Database/SQLAlchemy/author_book_publisher.db')

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)


    # Get the number of books printed by each publisher
    books_by_publisher = get_books_by_publishers(session, ascending=False)
    for row in books_by_publisher:
        print(f"Publisher: {row.name}, total books: {row.total_books}")
    print()

    # Get the number of authors each publisher publishes
    authors_by_publisher = get_authors_by_publishers(session)
    for row in authors_by_publisher:
        print(f"Publisher: {row.name}, total authors: {row.total_authors}")
    print()

    # Output hierarchical author data
    authors = get_authors(session)
    # output_author_hierarchy(authors)

    # Add a new book
    add_new_book(
        session,
        author_name="Stephen King",
        book_title="The Stand",
        publisher_name="Random House",
    )
    # Output the updated hierarchical author data
    authors = get_authors(session)
    # output_author_hierarchy(authors)

if __name__ == '__main__':  
    main()