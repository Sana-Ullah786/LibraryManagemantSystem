import { ReactElement, useState } from "react";
import { useHistory, useParams } from "react-router-dom";
import { useEffect, useContext } from "react";
import { client } from "../../axios";
import { BorrowedIn, BorrowedOut } from "../../CustomTypes";
import BorrowForm from "../BorrowForm";
import { AuthContext } from "../../contexts/AuthContext";

/**
 * The BorrowUpdate component displays a form for updating book details.
 * @returns The component to be rendered
 */
function BorrowUpdate(): ReactElement {
  const history = useHistory();
  let { id }: { id: string } = useParams(); // id is extracted from url

  // Fetching the book to be edited
  const [currBorrowed, setCurrBorrowed] = useState<BorrowedIn | undefined>();

  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);

  // This effect fetches the book
  useEffect(() => {
    client
      .GetBorrowedDetails(id)
      .then((borrowResponse: BorrowedIn) => {
        setCurrBorrowed(borrowResponse);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [id]);

  /**
   * This function is called when user submits the form. It uses api call to
   * server and saves the changes that were made to book details.
   * Once updated, we navigate to the details page for the book.
   * @param book The updated details of the book that were entered into the form.
   */
  function submitHandler(borrowed: BorrowedOut) {
    if (borrowed) {
      client
        .UpdateBorrowed(id, borrowed)
        .then((bookId) => {
          history.push("/users/" + borrowed.userId);
        })
        .catch((error) => {
          alert(error);
        });
    } else {
      alert("Error! Book with this id does not exist");
    }
  }

  return (
    <div className="background-image">
      <div className="modal">
        {currBorrowed !== undefined && (
          <BorrowForm
            borrowed={currBorrowed}
            submitHandler={submitHandler}
            isLibrarian={isLibrarian}
          ></BorrowForm>
        )}
        {currBorrowed === undefined && <p>Invalid Id!</p>}
      </div>
    </div>
  );
}

export default BorrowUpdate;
