from sqlalchemy import Column, Integer, String, ForeignKey, Table #nhập các lớp, và Columntừ SQLAlchemy Integer, được sử dụng để giúp xác định các thuộc tính mô hình.StringForeignKeyTable
from sqlalchemy.orm import relationship, backref #nhập các đối tượng relationship()và backref, được sử dụng để tạo mối quan hệ giữa các đối tượng.
from sqlalchemy.ext.declarative import declarative_base #nhập declarative_baseđối tượng, đối tượng này kết nối công cụ cơ sở dữ liệu với chức năng SQLAlchemy của các mô hình.

#ạo lớp Base, là lớp mà tất cả các models kế thừa từ đó và cách chúng có được chức năng SQLAlchemy ORM
Base = declarative_base()

#tạo author_publisher: model quan hệ
author_publisher = Table(
    "author_publisher", #Tên bảng quan hệ
    Base.metadata, # cung cấp kết nối giữa chức năng SQLAlchemy và công cụ cơ sở dữ liệu.

    # Câu lệnh trên cho SQLAlchemy biết rằng có một cột trong bảng author_publisher được đặt tên author_id.
    # Loại của cột đó là Integer và author_id là một khóa ngoại liên quan đến khóa chính trong bảng author
    Column("author_id", Integer, ForeignKey("author.author_id")), # các cột dữ liệu
    Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),

    #Việc có cả hai author_id và publisher_id được định nghĩa trong author_publisher Table 
    # thể hiện sẽ tạo ra kết nối từ authorbảng đến publisherbảng và ngược lại, thiết lập mối quan hệ nhiều-nhiều.
)

#tạo book_publisher: model quan hệ
book_publisher = Table(
    "book_publisher",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book.book_id")),
    Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
)

# Các bảng dữ liệu cần tạo
class Author(Base):
    __tablename__ = "author"
    author_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    books = relationship("Book", backref=backref("author")) #Xác nhận có quan hệ với class Book, thư viện sẽ tìm author_id trong class book và trả về backref
    
    #secondary: cho biết kết nối với class Publisher thông qua 1 bảng phụ author_publisher
    #back_populates: cho biết rằng có một tập hợp bổ sung trong lớp Publisher được gọi authors.
    publishers = relationship("Publisher", secondary=author_publisher, back_populates="authors")

class Book(Base):
    __tablename__ = "book"
    book_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.author_id"))
    #Ví dụ: book = session.query(Book).filter_by(Book.title == "The Stand").one_or_none()
    #       print(f"Authors name: {book.author.first_name} {book.author.last_name}")
    # Sự tồn tại của thuộc tính author ở Book là do backref định nghĩa.
    # backref rất tiện dụng khi bạn cần tham chiếu đến phụ huynh và tất cả những gì bạn có là một cá thể con.
    title = Column(String)
    publishers = relationship("Publisher", secondary=book_publisher, back_populates="books")

class Publisher(Base):
    __tablename__ = "publisher"
    publisher_id = Column(Integer, primary_key=True)
    name = Column(String)
    authors = relationship( "Author", secondary=author_publisher, back_populates="publishers")
    books = relationship("Book", secondary=book_publisher, back_populates="publishers")