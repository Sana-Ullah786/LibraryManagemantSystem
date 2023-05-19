import { BookSaved } from "../../CustomTypes";
import { Link } from "react-router-dom";
import { Author } from "../../CustomTypes";
import LibrarianLinks from "../LibrarianLinks";

type BookDetailsPresentationProps = {
  isLibrarian: boolean;
  showLinks?: boolean;
  id: number;
  url: string;
  book: BookSaved;
};

const NOT_FOUND = "Not Found";

export const BookDetailsPresentation = (
  props: BookDetailsPresentationProps
) => {
  /*
   * BookDetailsPresentation is responsible for displaying all the details of book.
   * It receives the data as properties and does not have to perform any api calls or calculations.
   */

  return (
    <div>
      <h1>
        <p style={{ display: "inline" }} data-testid="titleHeading">
          {" "}
          Title:{" "}
        </p>
        <p style={{ display: "inline" }} data-testid="title">
          {" "}
          {props.book.title}{" "}
        </p>
      </h1>
      {props.isLibrarian && props.showLinks && (
        <>
          <LibrarianLinks url={props.url} />
          <br />
        </>
      )}
      <p style={{ display: "inline" }} data-testid="authorHeading">
        <strong>Authors: </strong>
      </p>
      <p data-testid="author" style={{ display: "inline" }}>
        {props.book.authors.map((author: Author) => (
          <Link to={"../authors/" + author.id}>
            {author.last_name + ", " + author.first_name}
          </Link>
        ))}
      </p>
      <br></br>
      <br></br>
      <p style={{ display: "inline" }} data-testid="descriptionHeading">
        <strong>Description: </strong>
      </p>
      <p data-testid="description" style={{ display: "inline" }}>
        {" "}
        {props.book.description}
      </p>
      <br></br>
      <br></br>
      <p style={{ display: "inline" }} data-testid="isbnHeading">
        <strong>ISBN: </strong>
      </p>
      <p data-testid="isbn" style={{ display: "inline" }}>
        {" "}
        {props.book.isbn}
      </p>
      <br></br>
      <br></br>
      <p style={{ display: "inline" }} data-testid="languageHeading">
        <strong>Language: </strong>
      </p>
      <p data-testid="language" style={{ display: "inline" }}>
        {props.book.language !== undefined
          ? props.book.language.language
          : NOT_FOUND}
      </p>
      <br></br>
      <br></br>
      <p style={{ display: "inline" }} data-testid="genreHeading">
        <strong>Genre: </strong>
      </p>
      <p data-testid="genres" style={{ display: "inline" }}>
        {" "}
        {Object.values(props.book.genres)
          .map((genre) => genre.genre)
          .join(", ")}
      </p>
      <br></br>
      <br></br>
      <p style={{ display: "inline" }} data-testid="dateOfPublicationHeading">
        <strong>Date of Publication: </strong>
      </p>
      <p data-testid="dateOfPublication" style={{ display: "inline" }}>
        {props.book.dateOfPublication.toISOString().substring(0, 10)}
      </p>
    </div>
  );
};

// By default, links are always shown if the user is librarian
BookDetailsPresentation.defaultProps = { showLinks: true };
