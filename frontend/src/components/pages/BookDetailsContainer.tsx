import React, { useEffect, useState, useContext } from "react";
import { BookSaved, ErrorObject } from "../../CustomTypes";
import { useParams } from "react-router";
import { BookDetailsPresentation } from "./BookDetailsPresentation";
import { client } from "../../axios";
import { AuthContext } from "../../contexts/AuthContext";
import { useRouteMatch } from "react-router-dom";
import ErrorComponent from "../ErrorComponent";

export const BookDetailsContainer = (props: { showLinks?: boolean }) => {
  /*
   * BookDetailsContainer performs all the computation and api calls to fetch book details.
   * It delegates the task of actually displaying the data to BookDetailsPresentation.
   */

  //id is extracted from url
  let { id }: { id: string } = useParams();

  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  let { url }: { url: string } = useRouteMatch(); // The url of this page

  // book, genre and language are intentially allowed to be undefined. We display the page once these values are loaded

  let [book, setBook]: [
    BookSaved | undefined,
    React.Dispatch<React.SetStateAction<BookSaved | undefined>>
  ] = useState(); //The book to be displayed

  const [error, setError] = useState<ErrorObject>();

  useEffect(() => {
    // Getting value of book from the api
    client
      .GetBookDetails(id)
      .then(
        (bookDetails: BookSaved) => {
          setBook(bookDetails);
        }
        //(error) => { console.log(`Error! The book with id ${id} does not exist.`); }
      )
      .catch((err) => {
        setError(err);
      });
  }, [id]);

  if (!book) {
    if (error) {
      return <ErrorComponent error={error} />;
    }
    return <div>Loading...</div>;
  } else {
    // The book details are presented once all details have been received
    return (
      <>
      <div className="background-image"></div>
      <div className="modal">
        <BookDetailsPresentation
          url={url}
          showLinks={props.showLinks}
          isLibrarian={isLibrarian}
          id={parseInt(id)}
          book={book}
        />
        </div>  
      </>
    );
  }
};

// By default links are always shown if the user is a librarian
BookDetailsContainer.defaultProps = { showLinks: true };
