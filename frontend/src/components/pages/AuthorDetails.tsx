import React, { useEffect, useState, useContext } from "react";
import { useParams, Link, useRouteMatch } from "react-router-dom";

import { client } from "../../axios";
import { AuthContext } from "../../contexts/AuthContext";
import { BookSaved, ErrorObject } from "../../CustomTypes";
import ErrorComponent from "../ErrorComponent";
import { BookListPresentation } from "./BookListPresentation";
import { Pagination } from './pagination';

function AuthorDetails() {
  //Getting the id of the author from the url of the current page as a parameter
  let { id }: { id: string } = useParams();
  const { url }: { url: string } = useRouteMatch();
  const [page, setPage] = useState<number>(1);
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);

  const [firstName, setFirstName] = useState<string | null | undefined>("");
  const [lastName, setLastName] = useState<string | null | undefined>("");
  const [dateOfBirth, setDateOfBirth] = useState<string | null | undefined>("");
  const [dateOfDeath, setDateOfDeath] = useState<string | null | undefined>("");
  const [books, setBooks] = useState<BookSaved[]>([]);
  const [error, setError] = useState<ErrorObject>();

  //Getting the details of a specific author from the api endpoint
  useEffect(() => {
    client
      .GetAuthorDetails(id)
      .then(
        (response) => {
          if (response) {
            setFirstName(response.first_name);
            setLastName(response.last_name);
            setDateOfBirth(response.birth_date);
            setDateOfDeath(response.death_date);
          }
        },
        (error) => {
          setError(error);
        }
      )
      .catch((error) => {
        setError(error);
      });
    client
      .GetBooksForAuthor(id)
      .then((bookList) => {
        setBooks(bookList);
      })
      .catch((error) => {
        setError(error);
      });
  }, [id]);

  //This creates links to the update and delete librarian pages
  function librarianLinks() {
    return (
      <div style={{display:'flex', justifyContent:'center'}}>
        <Link to={`${url}/update`} className="genre-list-update-button">
          {' '}
          Update{' '}
        </Link>
        <Link to={`${url}/delete`} className="genre-list-delete-button">
          Delete
        </Link>
      </div>
    );
  }

  //Rendering out the Author page.
  //The Book Description portion is a placeholder as the api to get the books for an author has not been made yet
  if (error != null) {
    return <ErrorComponent error={error} />;
  }

  return (
    <div className='background-image'>
      <div className="modal">
        <h1>
        Author: {lastName}, {firstName}
      </h1>
      {isLibrarian === true ? librarianLinks() : null}
      <p>
        ({dateOfBirth ? dateOfBirth.substring(0, 10).replace(/-/g, "/") : "-"}{" "}
        to {dateOfDeath ? dateOfDeath.substring(0, 10).replace(/-/g, "/") : "-"}
        )
      </p>
      <div>
        <h3>Books</h3>
        <BookListPresentation showLinks={false} books={books} url={url} />
      </div>
    </div>
    </div>

  );
}

export default AuthorDetails;
