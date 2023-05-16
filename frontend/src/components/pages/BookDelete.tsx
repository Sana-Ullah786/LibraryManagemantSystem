import { useHistory, useParams } from "react-router-dom";
import { ReactElement } from "react";
import { client } from "../../axios";
import { BookDetailsContainer } from "./BookDetailsContainer";

/**
 * The BookDelete component displays book deletion page.
 * The id of the book to be deleted is fetched from url.
 * @returns The component to be rendered
 */
function BookDelete(): ReactElement {
  let { id }: { id: string } = useParams(); // extracting id from url
  const history = useHistory();

  /**
   * This function is called when user presses the delete button.
   * Once clicked, the book is deleted using api call to the server.
   * After deletion, we navigate to book list page.
   */
  function handleClick() {
    client
      .DeleteBook(id)
      .then((response) => {
        history.push("/books");
      })
      .catch((error) => {
        alert("A book with this id does not exist");
      });
  }

  return (
    <div>
      <h1>DELETE Book?</h1>
      {/* Displaying the book details component to show which book is being deleted */}
      <BookDetailsContainer showLinks={false} />
      <button onClick={handleClick}>Yes, Delete</button>
    </div>
  );
}

export default BookDelete;
