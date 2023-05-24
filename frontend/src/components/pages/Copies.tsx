import React, { useEffect, useState, useContext } from "react";
import { BookIn, CopyIn, ErrorObject } from "../../CustomTypes";
import { useParams } from "react-router";
import { BookDetailsPresentation } from "./BookDetailsPresentation";
import { client } from "../../axios";
import { AuthContext } from "../../contexts/AuthContext";
import { useRouteMatch, Link } from "react-router-dom";
import ErrorComponent from "../ErrorComponent";
import LibrarianLinks from "../LibrarianLinks";

const Copies = (props: { showLinks?: boolean }) => {
  /*
   * BookDetailsContainer performs all the computation and api calls to fetch book details.
   * It delegates the task of actually displaying the data to BookDetailsPresentation.
   */

  //id is extracted from url
  let { id }: { id: string } = useParams();

  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  let { url }: { url: string } = useRouteMatch(); // The url of this page

  // book, genre and language are intentially allowed to be undefined. We display the page once these values are loaded

  let [copies, setCopies]: [
    CopyIn[] | undefined,
    React.Dispatch<React.SetStateAction<CopyIn[] | undefined>>
  ] = useState(); //The copies to be displayed
  let [book, setBook]: [
    BookIn | undefined,
    React.Dispatch<React.SetStateAction<BookIn | undefined>>
  ] = useState();

  const [error, setError] = useState<ErrorObject>();

  useEffect(() => {
    // Getting value of book from the api
    client
      .GetCopiesofBook(id)
      .then(
        (newCopies: CopyIn[]) => {
          newCopies.sort((a, b) => (a.id > b.id ? 1 : -1));
          setCopies(newCopies);
          if (newCopies.length > 0) {
            setBook(newCopies[0].book);
          }
        }
        //(error) => { console.log(`Error! The book with id ${id} does not exist.`); }
      )
      .catch((err) => {
        setError(err);
      });
  }, [id]);

  console.log(copies);

  if (copies?.length === 0) {
    if (error) {
      return <ErrorComponent error={error} />;
    }
    return <div>Loading...</div>;
  } else {
    // The book details are presented once all details have been received
    return (
      <div className="background-image">
        <h1>Copies for {book?.title}</h1>
        <ul>
          {copies?.map((copy: CopyIn, index: number) => (
            <li>
              <h2>Copy {index + 1}</h2>
              <p>Status: {copy.status.status}</p>
              <p>Language: {copy.language.language}</p>
              {isLibrarian && <LibrarianLinks url={`/copies/${copy.id}`} />}
            </li>
          ))}
        </ul>
        {isLibrarian && (
          <Link to={`/books/${id}/copies/add`} className="genre-link">
            Add Copy
          </Link>
        )}
      </div>
    );
  }
};

// By default links are always shown if the user is a librarian
Copies.defaultProps = { showLinks: true };

export default Copies;
