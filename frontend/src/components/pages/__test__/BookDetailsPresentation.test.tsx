import { render, cleanup } from "@testing-library/react";
import { BookDetailsPresentation } from "../BookDetailsPresentation";
import { Book, AuthorAttributes, Genre, Language } from "../../../CustomTypes";
import { StaticRouter } from "react-router-dom";
import renderer from "react-test-renderer";
//TODO: Changes to the custom types file means that these test cases won't work anymore and will need to be changed
const book: Book = {
  id: 1,
  title: "title",
  authorId: 1,
  description: "description",
  isbn: "1231231231231",
  languageId: 1,
  genreIds: [1, 2],
};

const author: AuthorAttributes = {
  id: 1,
  first_name: "firstname",
  last_name: "lastname",
  birth_date: "dateofbirth",
  death_date: "dateofdeath",
};

const language: Language = {
  id: 1,
  name: "English",
};

const genres: Genre[] = [
  {
    id: 1,
    name: "Fantasy",
  },
  {
    id: 2,
    name: "Drama",
  },
];

// Cleans up the DOM after each test
afterEach(cleanup);

/**
 * These tests check if the books page renders with correct fomat and text for
 * book attribute headings
 */
describe("Tests correct correct rendering of style and headings", () => {
  /**
   * This test checks if the component renders without any errors.
   */
  test("renders without error", () => {
    render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );
  });

  /**
   * This test checks if the text of title heading is correct
   */
  test("renders correct heading for title", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );

    expect(getByTestId("titleHeading")).toHaveTextContent("Title:");
  });

  /**
   * This test checks if the text of title heading is correct
   */
  test("renders correct heading for author", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );

    expect(getByTestId("authorHeading")).toHaveTextContent("Author:");
  });

  /**
   * This test checks if the text of description heading is correct
   */
  test("renders correct heading for description", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );

    expect(getByTestId("descriptionHeading")).toHaveTextContent("Description:");
  });

  /**
   * This test checks if the text of isbn heading is correct
   */
  test("renders correct heading for isbn", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );

    expect(getByTestId("isbnHeading")).toHaveTextContent("ISBN:");
  });

  /**
   * This test checks if the text of language heading is correct
   */
  test("renders correct heading for language", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );

    expect(getByTestId("languageHeading")).toHaveTextContent("Language:");
  });

  /**
   * This test checks if the text of genre heading is correct
   */
  test("renders correct heading for genre", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );

    expect(getByTestId("genreHeading")).toHaveTextContent("Genre:");
  });

  /**
   * This test checks if the child of author heading is strong
   */
  test("renders correct style for author heading", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );

    const authorHeading = getByTestId("authorHeading");
    expect(authorHeading.firstElementChild?.tagName).toBe("STRONG");
  });

  /**
   * This test checks if the child of genre heading is strong
   */
  test("renders correct style for genre heading", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );

    const genreHeading = getByTestId("genreHeading");
    expect(genreHeading.firstElementChild?.tagName).toBe("STRONG");
  });
});

/**
 * These tests check if correct data is displayed for each book attribute
 */
describe("Tests correct data displayed for each heading", () => {
  /**
   * This test checks if book title is correctly displayed
   */
  test("renders correct title for book", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );

    expect(getByTestId("title")).toHaveTextContent(book.title);
  });

  /**
   * This test checks if author text is correct
   */
  test("renders correct author name", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );
    expect(getByTestId("author")).toHaveTextContent(
      author.last_name + ", " + author.first_name
    );
  });

  /**
   * This test checks if description has correct text
   */
  test("renders correct description text", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );
    expect(getByTestId("description")).toHaveTextContent(book.description);
  });

  /**
   * This test checks if language has correct text
   */
  test("renders correct language text", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );
    expect(getByTestId("language")).toHaveTextContent(language.name);
  });

  /**
   * This test checks if genres have correct text
   */
  test("renders correct genres text", () => {
    const { getByTestId } = render(
      <StaticRouter>
        <BookDetailsPresentation
          book={book}
          author={author}
          language={language}
          genres={genres}
        />
      </StaticRouter>
    );

    expect(getByTestId("genres")).toHaveTextContent(
      Object.values(genres)
        .map((genre) => genre.name)
        .join(", ")
    );
  });
});

/**
 * These tests check the snapshot for the rendered elements.
 */
describe("Snapshot tests", () => {
  /**
   * This test makes sure that the snapshot produced is valid and up to date.
   * It detects any changes in user interface and reports them.
   */
  test("produces correct snapshot", () => {
    const tree = renderer
      .create(
        <StaticRouter>
          <BookDetailsPresentation
            book={book}
            author={author}
            language={language}
            genres={genres}
          />
        </StaticRouter>
      )
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
