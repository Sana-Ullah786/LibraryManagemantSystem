import { useHistory, useParams } from "react-router-dom";
import { ReactElement, useEffect, useState } from "react";
import { client } from "../../axios";
import { CopyIn } from "../../CustomTypes";
/**
 * The CopyDelete component displays copy deletion page.
 * The id of the copy to be deleted is fetched from url.
 * @returns The component to be rendered
 */
function CopyDelete(): ReactElement {
  let { id }: { id: string } = useParams(); // extracting id from url
  const history = useHistory();

  let [currCopy, setCurrCopy]: [
    CopyIn | undefined,
    React.Dispatch<React.SetStateAction<CopyIn | undefined>>
  ] = useState();

  /**
   * This function is called when user presses the delete button.
   * Once clicked, the copy is deleted using api call to the server.
   * After deletion, we navigate to copy list page.
   */
  function handleClick() {
    client
      .DeleteCopy(id)
      .then((response) => {
        history.push(`/books/${currCopy?.book.id}/copies`);
      })
      .catch((error) => {
        alert("A copy with this id does not exist");
      });
  }

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

  return (
    <div className="background-image">
      <div className="modal">
        <h1>DELETE Copy?</h1>
        {/* Displaying the copy details component to show which copy is being deleted */}
        <h2>Copy for {currCopy?.book.title}</h2>
        <p>Status: {currCopy?.status.status}</p>
        <p>Language: {currCopy?.language.language}</p>
        <button className="genre-list-delete-button" onClick={handleClick}>
          Yes, Delete
        </button>
      </div>
    </div>
  );
}

export default CopyDelete;
