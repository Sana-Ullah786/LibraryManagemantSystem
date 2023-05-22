import React, { useState, useEffect, useContext } from "react";
import { client } from "../../axios";
import { useRouteMatch } from "react-router";
import { BookListPresentation } from "./BookListPresentation";
import { BookIn, ErrorObject } from "../../CustomTypes";
import ErrorComponent from "../ErrorComponent";
import { AuthContext } from "../../contexts/AuthContext";

export const BookListContainer = () => {
  /*
   * BookListContainer is responsible for all computations and api calls to fetch the list of all books.
   * Once all details are fetched, it delegates the task of presention to BookListPresentation.
   */

  let { url }: { url: string } = useRouteMatch(); // The url of this page
  let [books, setBooks]: [
    BookIn[] | undefined,
    React.Dispatch<React.SetStateAction<BookIn[] | undefined>>
  ] = useState(); // The list of books
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  console.log(isLibrarian);
  const [error, setError] = useState<ErrorObject>();

  useEffect(() => {
    client
      .GetBookList()
      .then((bookList) => {
        setBooks(bookList);
      })
      .catch((err) => {
        setError(err);
      });
  }, []);

  if (!books) {
    if (error) {
      return <ErrorComponent error={error} />;
    }
    return <div>Loading...</div>;
  }
  return (
    <>
      {/* Book list is presented once the list of books is properly initialized */}
      <BookListPresentation showLinks={isLibrarian} books={books} url={url} />
    </>
  );
};
