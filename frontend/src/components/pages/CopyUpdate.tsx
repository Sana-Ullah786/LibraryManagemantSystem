import { ReactElement, useState } from "react";
import { useHistory, useParams } from "react-router-dom";
import { useEffect } from "react";
import { client } from "../../axios";
import { CopyIn, CopyOut } from "../../CustomTypes";
import CopyForm from "../CopyForm";
/**
 * The BookUpdate component displays a form for updating book details.
 * @returns The component to be rendered
 */
function CopyUpdate(): ReactElement {
  const history = useHistory();
  let { id }: { id: string } = useParams(); // id is extracted from url

  // Fetching the book to be edited
  let [currCopy, setCurrCopy]: [
    CopyIn | undefined,
    React.Dispatch<React.SetStateAction<CopyIn | undefined>>
  ] = useState();

  // This effect fetches the book
  useEffect(() => {
    client
      .GetCopyDetails(id)
      .then((copyResponse: CopyIn) => {
        setCurrCopy(copyResponse);
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
  function submitHandler(copy: CopyOut) {
    if (currCopy) {
      client
        .UpdateCopy(copy, currCopy.id)
        .then((copyId) => {
          history.push(`/books/${currCopy?.book.id}/copies`);
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
        {currCopy !== undefined && (
          <CopyForm copy={currCopy} submitHandler={submitHandler}></CopyForm>
        )}
        {currCopy === undefined && <p>Invalid Id!</p>}
      </div>
    </div>
  );
}

export default CopyUpdate;
