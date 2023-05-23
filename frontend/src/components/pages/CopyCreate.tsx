import { useHistory, useParams } from "react-router-dom";
import { ReactElement, useEffect, useState } from "react";
import { client } from "../../axios";
import { CopyOut, CopyIn, BookIn, ErrorObject } from "../../CustomTypes";
import CopyForm from "../CopyForm";
import ErrorComponent from "../ErrorComponent";

/**
 * The BookCreate component creates a form for book creation.
 * @returns The component to be rendered
 */
function CopyCreate(): ReactElement {
  const history = useHistory();
  const { id }: { id: string } = useParams();

  console.log("here");

  let [book, setBook]: [
    BookIn | undefined,
    React.Dispatch<React.SetStateAction<BookIn | undefined>>
  ] = useState(); //The book to be displayed

  const [error, setError] = useState<ErrorObject>();

  useEffect(() => {
    // Getting value of book from the api
    client
      .GetBookDetails(id)
      .then(
        (bookDetails: BookIn) => {
          setBook(bookDetails);
        }
        //(error) => { console.log(`Error! The book with id ${id} does not exist.`); }
      )
      .catch((err) => {
        setError(err);
      });
  }, [id]);

  function submitHandler(copy: CopyOut) {
    client
      .CreateCopy(copy)
      .then((id: number) => {
        history.push(`/books/${book?.id}/copies`);
      })
      .catch((error) => {
        alert(error);
      });
  }
  if (!book) {
    if (error) {
      return <ErrorComponent error={error} />;
    }
    return <div>Loading...</div>;
  } else {
    return (
      <div className="background-image">
        <CopyForm
          copy={{
            id: -1,
            language: book.language,
            book: book,
            status: { status: "", id: -1 },
          }}
          submitHandler={submitHandler}
        ></CopyForm>
      </div>
    );
  }
}

export default CopyCreate;
