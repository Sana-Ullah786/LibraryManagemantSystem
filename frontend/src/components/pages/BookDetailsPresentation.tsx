import { Book } from '../../CustomTypes'
import { Link } from 'react-router-dom'
import { Author } from '../../CustomTypes';
import LibrarianLinks from '../LibrarianLinks';
import { GenreMap, Language } from '../../CustomTypes';

type BookDetailsPresentationProps = {
    isLibrarian: boolean;
    showLinks?: boolean;
    id: number;
    url: string;
    book: Book;
    author?: Author;
    language?: Language;
    genres: GenreMap;
}

const NOT_FOUND = "Not Found";

export const BookDetailsPresentation = (props: BookDetailsPresentationProps) => {

    /*
    * BookDetailsPresentation is responsible for displaying all the details of book.
    * It receives the data as properties and does not have to perform any api calls or calculations.
    */


    return (

        <div>

            <h1>
                <p style={{ display:"inline" }} data-testid="titleHeading"> Title: </p>
                <p style={{ display:"inline" }} data-testid="title"> {props.book.title} </p>    
            </h1>
            {
                props.isLibrarian && props.showLinks && (
                    <>
                        <LibrarianLinks url={props.url} />
                        <br />
                    </>
                )
            }
            <p style={{ display:"inline" }} data-testid="authorHeading">
                <strong>Author: </strong>
            </p>
            <p data-testid="author" style={{ display:"inline" }}>
                {
                    props.author?
                    <Link to={"../authors/" + props.book.authorId}>
                        {props.author.last_name + ", " + props.author.first_name}
                    </Link>
                    : NOT_FOUND
                }
            </p>
            <br></br>
            <br></br>
            <p style={{ display:"inline" }} data-testid="summaryHeading"><strong>Summary: </strong></p>
            <p data-testid="summary" style={{ display:"inline" }}> {props.book.summary}</p>
            <br></br>
            <br></br>
            <p style={{ display:"inline" }} data-testid="isbnHeading"><strong>ISBN: </strong></p>
            <p data-testid="isbn" style={{ display:"inline" }}> {props.book.isbn}</p>
            <br></br>
            <br></br>
            <p style={{ display:"inline" }} data-testid="languageHeading"><strong>Language: </strong></p>
            <p data-testid="language" style={{ display:"inline" }}>
                {
                    props.language !== undefined?
                    props.language.name
                    : NOT_FOUND
                }
            </p>
            <br></br>
            <br></br>
            <p style={{ display:"inline" }} data-testid="genreHeading"><strong>Genre: </strong></p>
            <p data-testid="genres" style={{ display:"inline" }}> {Object.values(props.genres).map((genre) => genre.name).join(", ")}</p>

        </div>
    );


}

// By default, links are always shown if the user is librarian
BookDetailsPresentation.defaultProps = {showLinks: true}

