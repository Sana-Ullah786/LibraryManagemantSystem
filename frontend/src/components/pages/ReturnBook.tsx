import React, { ReactElement, useEffect, useState, useContext } from "react";
import { useParams, useHistory } from "react-router-dom";
import { client } from "../../axios";
import { ErrorObject } from "../../CustomTypes";
import ErrorComponent from "../ErrorComponent";
import { AuthContext } from "../../contexts/AuthContext";
import "../style.css"; // Import the Languages CSS file
import { BorrowedIn } from "../../CustomTypes";

interface Props {}

function ReturnBook(props: Props): ReactElement {
  const { id }: { id: string } = useParams();
  const history = useHistory();
  const [borrowed, setBorrowed] = useState<BorrowedIn | undefined>();
  const [error, setError] = useState<ErrorObject>();
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  const { isAuthenticated }: { isAuthenticated: boolean } =
    useContext(AuthContext);

  useEffect(() => {
    client
      .GetBorrowedDetails(id)
      .then((borrowedData) => {
        setBorrowed(borrowedData);
      })
      .catch((error) => {
        setError(error);
      });
  }, [id]);

  useEffect(() => {
    if (isAuthenticated !== true) {
      let err: ErrorObject = {
        status: 401,
        message: "Unauthorized, you must be logged in to view this page",
      };
      setError(err);
    }
  }, [isAuthenticated]);

  function handleReturn() {
    if (borrowed !== undefined) {
      client
        .ReturnBorrowed(id, {
          ...borrowed,
          copyId: borrowed.copy.id,
          userId: borrowed.user.id,
        })
        .then((response) => {
          history.push("/my_borrowed");
        });
    }
  }

  if (error != null) {
    return <ErrorComponent error={error} />;
  }

  return (
    <div className="background-image">
      <div className="signup-form">
        {borrowed !== undefined ? (
          <>
            <h2>Return book: {borrowed?.copy.book.title}</h2>
            <button onClick={handleReturn} className="language-action-button">
              Return
            </button>
          </>
        ) : (
          <h2>Loading...</h2>
        )}
      </div>
    </div>
  );
}

export default ReturnBook;
