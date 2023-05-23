import { Link } from "react-router-dom";
import { BookIn } from "../../CustomTypes";
import LibrarianLinks from "../LibrarianLinks";
import "../style.css"; // Import the Genres CSS file

export const BookListPresentation = (props: {
  books: BookIn[];
  url: string;
  showLinks: boolean;
}) => {
  /*
   * BookListPresentation displays the list of books. It does not have to perform any api calls
   * or computations. It simply displays the content received as properties.
   */

  return (
    <div>
      <ul>
        {props.books.map((book) => (
          <li
            key={book.id.toString()}
            data-testid={"item" + book.id.toString()}
          >
            <Link to={"/books/" + book.id.toString()}>{book.title}</Link>

            {props.showLinks && (
              <LibrarianLinks url={`${props.url}/${book.id}`} />
            )}
          </li>
        ))}
      </ul>
      {props.showLinks && (
        <>
          <Link to={`${props.url}/create`}> Create Book </Link>
        </>
      )}
    </div>
  );
};
