import React, { useEffect, useState, useContext } from "react";
import { BorrowedIn, ErrorObject } from "../../CustomTypes";
import { useParams } from "react-router";
import { client } from "../../axios";
import { AuthContext } from "../../contexts/AuthContext";
import { useRouteMatch, Link } from "react-router-dom";
import ErrorComponent from "../ErrorComponent";

const MyBorrowed = (props: { showLinks?: boolean }) => {
  /*
   * BookDetailsContainer performs all the computation and api calls to fetch book details.
   * It delegates the task of actually displaying the data to BookDetailsPresentation.
   */

  //id is extracted from url
  let { id }: { id: string } = useParams();

  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  let { url }: { url: string } = useRouteMatch(); // The url of this page

  // book, genre and language are intentially allowed to be undefined. We display the page once these values are loaded

  let [myBorrowed, setMyBorrowed]: [
    BorrowedIn[] | undefined,
    React.Dispatch<React.SetStateAction<BorrowedIn[] | undefined>>
  ] = useState(); //The myBorrowed to be displayed

  const [error, setError] = useState<ErrorObject>();

  useEffect(() => {
    // Getting value of book from the api
    client
      .GetMyBorrowed()
      .then(
        (newMyBorrowed: BorrowedIn[]) => {
          newMyBorrowed.sort((a, b) => (a.id > b.id ? 1 : -1));
          setMyBorrowed(newMyBorrowed);
        }
        //(error) => { console.log(`Error! The book with id ${id} does not exist.`); }
      )
      .catch((err) => {
        setError(err);
      });
  }, [id]);

  console.log(myBorrowed);

  if (myBorrowed?.length === 0) {
    if (error) {
      return <ErrorComponent error={error} />;
    }
    return <div>Loading...</div>;
  } else {
    // The book details are presented once all details have been received
    return (
      <div className="background-image">
        <div className="modal">
          <h1>My Borrowed Books</h1>
          <ul>
            {myBorrowed?.map((borrowed: BorrowedIn, index: number) => (
              <li>
                <h2>{borrowed.copy.book.title}</h2>
                <p>Issue Date: {borrowed.issueDate}</p>
                <p>Due Date: {borrowed.dueDate}</p>
                <p>Return Date: {borrowed.returnDate}</p>
                {borrowed.returnDate && (
                  <Link to={`/borrowed/${borrowed.id}/return`}>Return</Link>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  }
};

// By default links are always shown if the user is a librarian
MyBorrowed.defaultProps = { showLinks: true };

export default MyBorrowed;
