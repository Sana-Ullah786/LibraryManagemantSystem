import { render, cleanup } from '@testing-library/react';
import { BookListPresentation } from '../BookListPresentation';
import { Book, AuthorAttributes, Genre, Language } from '../../../CustomTypes';
import { StaticRouter } from 'react-router-dom';
import renderer from 'react-test-renderer';

//TODO: changes to the custom types file means these test cases won't work anymore and will need to be changed
const books: Book[] = [
    {
        id: 1,
        title: 'title1',
        authorId: 1,
        summary: 'summary',
        isbn: '1231231231231',
        languageId: 1,
        genreIds: [1, 2]
    },
    {
        id: 2,
        title: 'title2',
        authorId: 1,
        summary: 'summary',
        isbn: '1231231231231',
        languageId: 1,
        genreIds: [2]
    }
];

const author: AuthorAttributes = {
    id: 1,
    first_name: 'firstname',
    last_name: 'lastname',
    date_of_birth: 'dateofbirth',
    date_of_death: 'dateofdeath' 
};

const language: Language = {
    id: 1,
    name: 'English'
};

const genres: Genre[] = [
    {
        id: 1,
        name: 'Fantasy'
    },
    {
        id: 2,
        name: 'Drama'
    }
];

afterEach(cleanup);


describe("renders correct content", () => {

    /**
     * This test checks if the component renders without any errors.
     */
    test('renders without error', () => {

        render(
            < StaticRouter >
                <BookListPresentation books={ books } url={ "test-url" }/>
            </StaticRouter>
        );

    });

    /**
     * This test checks that each list item contains a Link element
     */
    test("attaches a link to each list item", () => {

        const { getByTestId } = render(
            < StaticRouter >
                <BookListPresentation books={ books } url={ "test-url" }/>
            </StaticRouter>
        );

        for(const book of books){
            expect(getByTestId("item" + book.id).firstElementChild?.tagName).toBe("A");
        }

    });

    /**
     * This test checks that each list item contains the correct url
     */
     test("attaches correct url to each link", () => {

        const { getByTestId } = render(
            < StaticRouter >
                <BookListPresentation books={ books } url={ "test-url" }/>
            </StaticRouter>
        );

        for(const book of books){
            expect(getByTestId("item" + book.id).firstElementChild).toHaveAttribute("href", "/test-url/" + book.id);
        }

    });

});


describe("tests correct data displayed", () => {

    /**
    * This test checks that correct text is displayed for each item
    */
    test("correct text displayed", () => {

        const { getByTestId } = render(
            < StaticRouter >
                <BookListPresentation books={ books } url={ "test-url" }/>
            </StaticRouter>
        );

        for(const book of books){
            expect(getByTestId("item" + book.id)).toHaveTextContent(book.title);
        }

    });

});

describe("Snapshot tests", () => {

    /**
     * This test makes sure that the snapshot produced is valid and up to date.
     * It detects any changes in user interface and reports them.
     */
    test("produces correct snapshot", () => {

        const tree = renderer
            .create(
                < StaticRouter >
                    <BookListPresentation books={ books } url={ "test-url" }/>
                </StaticRouter>
            )
            .toJSON();
        expect(tree).toMatchSnapshot();

    });

});