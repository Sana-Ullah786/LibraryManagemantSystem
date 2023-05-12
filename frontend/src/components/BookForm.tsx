import { ReactElement, useEffect, useState } from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { client } from "../axios";
import { Author, Book, Genre, Language } from "../CustomTypes";

/**
 * The BookForm component displays a form for getting all book details from user.
 * @param props The properties that were passed to this component.
 * @returns The rendered component.
 */
function BookForm(props: { book: Book, submitHandler: SubmitHandler<Book> }): ReactElement {

    // A form for book
    let { register, handleSubmit } = useForm<Book>({
        defaultValues: { ...props.book }
    });

    // Details of all authors present in the system.
    let [authors, setAuthors]: [Author[] | undefined,
        React.Dispatch<React.SetStateAction<Author[] | undefined>>] = useState()

    // Details of all genres present in the system.
    let [genres, setGenres]: [Genre[] | undefined,
        React.Dispatch<React.SetStateAction<Genre[] | undefined>>] = useState()

    // Details of all languages present in the system.
    let [languages, setLanguages]: [Language[] | undefined,
        React.Dispatch<React.SetStateAction<Language[] | undefined>>] = useState()

    // This effect fetches authors from backend
    useEffect(() => {

        client.GetAllAuthors()
            .then(
                (authors: Author[]) => {
                    setAuthors(authors);
                },
                (error) => { console.log(`Error! couldn't fetch authors`); }
            )

    }, []);

    // This effect fetches genres from backend
    useEffect(() => {

        client.GetAllGenres()
            .then(
                (genres: Genre[]) => {
                    setGenres(genres);
                },
                (error) => { console.log(`Error! couldn't fetch genres`); }
            )

    }, []);

    // This effect fetches languages from backend
    useEffect(() => {

        client.GetAllLanguages()
            .then(
                (languages: Language[]) => {
                    setLanguages(languages);
                },
                (error) => { console.log(`Error! couldn't fetch languages`); }
            )

    }, []);

    return (
        <div>
            <form onSubmit={handleSubmit(props.submitHandler)}>
                <label>Title
                    <input
                        {...register('title')}
                        type="text"
                        placeholder={"Title"}
                    />
                </label>
                <br></br>
                <label> Author
                    {
                        /* A dropdown menu for selecting from all authors */
                        authors &&
                        <select {...register('authorId')} id="authors">
                            {
                                authors.map((author) => {
                                    return (
                                        <option value={author.id} key={author.id}> {author.first_name} {author.last_name} </option>
                                    );
                                })
                            }
                        </select>
                    }
                    {
                        !authors &&
                        <>No Authors!</>
                    }
                </label>
                <br></br>
                <label>Summary
                    <input
                        {...register('summary')}
                        type="text"
                        placeholder={"Summary"}
                    />
                </label>
                <br></br>
                <label>ISBN
                    <input
                        {...register('isbn')}
                        type="number"
                        placeholder={"ISBN"}
                    />
                </label>
                <br></br>
                <label> Language
                    {
                        /* A dropdown menu for selecting from all languages */
                        languages &&
                        <select {...register('languageId')} id="languages">
                            {
                                languages.map((language) => {
                                    return (
                                        <option value={language.id} key={language.id}> {language.name} </option>
                                    );
                                })
                            }
                        </select>
                    }
                    {
                        !languages &&
                        <>No Languages!</>
                    }
                </label>
                <br></br>
                <label> Genre (multiple allowed)
                    {
                        /* A dropdown menu for selecting from all genres */
                        genres &&
                        <select multiple {...register('genreIds')} id="genres">
                            {
                                genres.map((genre) => {
                                    return (
                                        <option value={genre.id} key={genre.id}> {genre.name} </option>
                                    );
                                })
                            }
                        </select>
                    }
                    {
                        !languages &&
                        <>No Languages!</>
                    }
                </label>
                <br></br>
                <button>Submit</button>
            </form>
        </div>
    );
}

export default BookForm;