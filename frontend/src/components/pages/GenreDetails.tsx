import React, { useEffect, useState, useContext } from "react";
import { useParams, Link, useRouteMatch } from "react-router-dom";
import { client } from "../../axios";
import { AuthContext } from "../../contexts/AuthContext";
import { BookIn, ErrorObject } from "../../CustomTypes";
import ErrorComponent from "../ErrorComponent";
import { BookListPresentation } from "./BookListPresentation";
import { Pagination } from "./pagination";
function GenreDetails() {
  const { id }: { id: string } = useParams();
  const genreId: number = parseInt(id);

  const { url }: { url: string } = useRouteMatch();

  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  const [books, setBooks] = useState<BookIn[]>([]);
  const [genre, setGenre] = useState<string | null | undefined>("");
  const [error, setError] = useState<ErrorObject>();
  const [page, setPage] = useState<number>(1);
  useEffect(() => {
    client
      .GetGenreDetails(genreId)
      .then((response) => {
        if (response) {
          setGenre(response.genre);
        }
      })
      .catch((error) => {
        setError(error);
      });
    client
      .GetBooksForGenre(id)
      .then((bookList) => {
        setBooks(bookList);
      })
      .catch((error) => {
        setError(error);
      });
  }, [genreId]);

  function librarianLinks() {
    return (
      <>
        <Link to={`${url}/update`} style={{ color: "orange" }}>
          {" "}
          Update{" "}
        </Link>
        <Link to={`${url}/delete`} style={{ color: "red" }}>
          Delete
        </Link>
      </>
    );
  }

  if (error != null) {
    return <ErrorComponent error={error} />;
  }

  return (
    <div className="background-image">
      <div className="modal">
        <h1>Genre: {genre}</h1>
        {isLibrarian === true ? librarianLinks() : null}
        <div>
          <h3>Books</h3>
          <BookListPresentation showLinks={false} books={books} url={url} />
        </div>
      </div>
    </div>
  );
}

export default GenreDetails;
