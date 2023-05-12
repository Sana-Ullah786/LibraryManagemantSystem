import React, { useEffect, useState, useContext } from 'react'
import { 
    BookSaved, 
    GenreMap, 
    Language,
    ErrorObject,
} from '../../CustomTypes'
import { useParams } from 'react-router'
import { Author } from '../../CustomTypes'
import { BookDetailsPresentation } from './BookDetailsPresentation'
import { client } from '../../axios'
import {AuthContext} from "../../contexts/AuthContext"
import { useRouteMatch } from 'react-router-dom'
import ErrorComponent from '../ErrorComponent'


export const BookDetailsContainer = (props:{showLinks?: boolean}) => {
    /*
    * BookDetailsContainer performs all the computation and api calls to fetch book details.
    * It delegates the task of actually displaying the data to BookDetailsPresentation.
    */

    //id is extracted from url
    let { id }: { id: string } = useParams();

    const {isLibrarian}: {isLibrarian: boolean} = useContext(AuthContext)
    let { url }: { url: string } = useRouteMatch(); // The url of this page

    // book, genre and language are intentially allowed to be undefined. We display the page once these values are loaded


    let [book, setBook]: [BookSaved | undefined,
        React.Dispatch<React.SetStateAction<BookSaved | undefined>>] = useState(); //The book to be displayed

    let [genres, setGenres]:
        [GenreMap, React.Dispatch<React.SetStateAction<GenreMap>>] = useState({});  // Genre of the book

    let [author, setAuthor]: [Author | undefined,
        React.Dispatch<React.SetStateAction<Author | undefined>>] = useState();   // Author of the book

    let [language, setLanguage]: [Language | undefined,
        React.Dispatch<React.SetStateAction<Language | undefined>>] = useState(); // Language of the book

    const [error,setError] = useState<ErrorObject>()

    useEffect(() => {

        // Getting value of book from the api
        client.GetBookDetails(id)
            .then(
                (bookDetails: BookSaved) => {
                    setBook(bookDetails);
                },
                //(error) => { console.log(`Error! The book with id ${id} does not exist.`); }
            )
            .catch(err => {
                setError(err)
            })

    }, [id]);


    useEffect(() => {

        if (book) {
            // This effect takes action once the book is properly loaded

            // Fetching the author of this book from api
            client.GetAuthorDetails(String(book.authorId))
                .then(
                    (authorDetails: Author) => {
                        setAuthor(authorDetails);
                    },
                    //(errorAuthor) => { console.log(`Error! Author for book with id ${id} does not exist`); }
                )
                .catch(err => {
                    setError(err)
                })
        }


    }, [book, id]);


    useEffect(() => {

        if (book) {
            // This effect takes action once the book is properly loaded

            for (const genre of book.genreIds) {
                // Fetching each genre using a individual api calls

                client.GetGenreDetails(String(genre))
                    .then(
                        (genreDetails) => {
                            setGenres((prevGenres: GenreMap) => ({
                                ...prevGenres,
                                [genre]: genreDetails
                            }));   
                        },
                    )
                    .catch(err => {
                        setError(err)
                    })
            }
        }

    }, [book, id]);


    useEffect(() => {

        if (book) {
            // This effect takes action once the book is properly loaded

            // Fetching the language of this book using api
            client.GetLanguageDetails(String(book.languageId))
                .then(
                    (languageDetails) => {
                        setLanguage(languageDetails);
                    },
                )
                .catch(err => {
                    setError(err)
                })

        }

    }, [book, id]);
    


    if (!book || !author || !language) {
        if (error){
            return(
                <ErrorComponent error={error} />
            )
        }
        return <div>Loading...</div>
    }
    else {
        // The book details are presented once all details have been received
        return (
            <>
                <BookDetailsPresentation url={url} showLinks={props.showLinks} isLibrarian={isLibrarian} id={parseInt(id)}
                    book={book} author={author} language={language} genres={genres} />
            </>
        )
    }

}

// By default links are always shown if the user is a librarian
BookDetailsContainer.defaultProps = {showLinks: true}
