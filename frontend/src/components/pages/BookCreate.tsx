import { useHistory } from "react-router-dom";
import { ReactElement } from "react";
import { client } from "../../axios";
import { BookOut } from "../../CustomTypes";
import BookForm from "../BookForm";

/**
 * The BookCreate component creates a form for book creation.
 * @returns The component to be rendered
 */
function BookCreate(): ReactElement {
  const history = useHistory();

  /**
   * This function uses a post api call to save the book in backend server.
   * Once done, it navigates to the detailed page of created book.
   * @param book The book details that were entered in form
   */
  function submitHandler(book: BookOut) {
    client
      .CreateBook(book)
      .then((bookId) => {
        history.push("/books/" + bookId);
      })
      .catch((error) => {
        alert(error);
      });
  }

  return (
    <div className='background-image'>
          <BookForm
      book={{
        id: -1,
        title: "",
        authors: [],
        language: { language: "", id: -1 },
        genres: [],
        description: "",
        isbn: "",
        dateOfPublication: "",
      }}
      submitHandler={submitHandler}
    ></BookForm>
    </div>
  );
}

export default BookCreate;
