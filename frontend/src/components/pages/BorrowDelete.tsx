import React, { ReactElement, useEffect, useState, useContext } from "react";
import { useParams, useHistory } from "react-router-dom";
import { client } from "../../axios";
import { BorrowedIn, ErrorObject } from "../../CustomTypes";
import ErrorComponent from "../ErrorComponent";
import { AuthContext } from "../../contexts/AuthContext";
import "../style.css"; // Import the Genres CSS file

interface Props {}

function BorrowDelete(props: Props): ReactElement {
  let { id }: { id: string } = useParams();
  const history = useHistory();
  const [borrowed, setBorrowed] = useState<BorrowedIn | undefined>();
  const [error, setError] = useState<ErrorObject>();
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  const { isAuthenticated }: { isAuthenticated: boolean } =
    useContext(AuthContext);

  //We will make a get request to obtain the details of the author we are about to delete.
  useEffect(() => {
    client
      .GetBorrowedDetails(id)
      .then((borrowed) => {
        setBorrowed(borrowed);
      })
      .catch((error) => {
        setError(error);
      });
  }, [id]);

  useEffect(() => {
    if (isAuthenticated === true) {
      if (isLibrarian !== true) {
        let err: ErrorObject = {
          status: 403,
          message: "Forbidden. You do not have permission to view this page",
        };
        setError(err);
      }
    } else {
      let err: ErrorObject = {
        status: 401,
        message: "Unauthorized, you must be logged in to view this page",
      };
      setError(err);
    }
  }, [isAuthenticated, isLibrarian]);

  //Deleting the author and then redirecting to the /authors page upon success
  function handleClick() {
    client.DeleteBorrowed(id).then((response) => {
      history.goBack();
    });
  }
  if (error != null) {
    return <ErrorComponent error={error} />;
  }

  return (
    <div className="background-image">
      <h1>
        DELETE Borrow of {borrowed?.copy.book.title} for{" "}
        {borrowed?.user.first_name + " " + borrowed?.user.last_name} ?
      </h1>
      <button className="genre-list-danger-button" onClick={handleClick}>
        Yes, Delete
      </button>
    </div>
  );
}

export default BorrowDelete;
