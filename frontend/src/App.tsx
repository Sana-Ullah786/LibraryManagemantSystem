import "./App.css";
import Navbar from "./components/Navbar";
import Authors from "./components/pages/Authors";
import Home from "./components/pages/Home";
import Login from "./components/pages/Login";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import AuthContextProvider from "./contexts/AuthContext";
import AuthorDelete from "./components/pages/AuthorDelete";
import AuthorUpdate from "./components/pages/AuthorUpdate";
import AuthorCreate from "./components/pages/AuthorCreate";
import { BookListContainer } from "./components/pages/BookListContainer";
import { BookDetailsContainer } from "./components/pages/BookDetailsContainer";
import ErrorComponent from "./components/ErrorComponent";
import BookDelete from "./components/pages/BookDelete";
import BookUpdate from "./components/pages/BookUpdate";
import BookCreate from "./components/pages/BookCreate";
import Signup from "./components/pages/Signup";
import Genres from "./components/pages/Genres";
import GenreCreate from "./components/pages/GenreCreate";
import GenreUpdate from "./components/pages/GenreUpdate";
import GenreDetails from "./components/pages/GenreDetails";
import GenreDelete from "./components/pages/GenreDelete";
import Languages from "./components/pages/Languages";
import LanguageCreate from "./components/pages/LanguageCreate";
import LanguageDetails from "./components/pages/LanguageDetails";
import LanguageDelete from "./components/pages/LanguageDelete";
import LanguageUpdate from "./components/pages/LanguageUpdate";
import Users from "./components/pages/Users";
import UserDetails from "./components/pages/UserDetails";
import UserCreate from "./components/pages/UserCreate";
import UserUpdate from "./components/pages/UserUpdate";
import Copies from "./components/pages/Copies";
import CopyCreate from "./components/pages/CopyCreate";
import CopyUpdate from "./components/pages/CopyUpdate";
import CopyDelete from "./components/pages/CopyDelete";
import MyBorrowed from "./components/pages/MyBorrowed";
import BorrowBook from "./components/pages/BorrowBook";
import ReturnBorrowed from "./components/pages/ReturnBorrowed";
import BorrowUpdate from "./components/pages/BorrowUpdate";
import AuthorDetails from "./components/pages/AuthorDetails";
import LibrarianSignup from "./components/pages/LibrarianSignup";
function App() {
  return (
    /**
     * This section of the code uses the react router to allow the user to navigate to different pages
     */
    <Router>
      <div>
        {/**The Authorization context provider is passed to all of the components */}
        <AuthContextProvider>
          {/* The nav bar should be displayed on all the pages */}
          <Navbar />
          <Switch>
            {/* The relative URL for the home page */}
            <Route exact path="/">
              <Home />
            </Route>
            {/* Relative URL for the authors list page */}
            <Route exact path="/authors">
              <Authors />
            </Route>
            {/* URL for the Login Page */}
            <Route path="/Login">
              <Login />
            </Route>
            {/* URL for a specific authors Details page */}
            <Route exact path="/authors/:id(\d+)">
              <AuthorDetails />
            </Route>
            {/* URL for the deletion page of a specific author */}
            <Route exact path="/authors/:id(\d+)/delete">
              <AuthorDelete />
            </Route>
            {/* URL for the update page of a specific author */}
            <Route exact path="/authors/:id(\d+)/update">
              <AuthorUpdate />
            </Route>
            {/* URL for the author Creation page */}
            <Route exact path="/authors/create">
              <AuthorCreate />
            </Route>
            {/* URL for the book deletion page using its id */}
            <Route exact path="/books/:id(\d+)/delete">
              <BookDelete />
            </Route>
            {/* URL for the update page of a specific book */}
            <Route exact path="/books/:id(\d+)/update">
              <BookUpdate />
            </Route>
            <Route exact path="/books/:id(\d+)/borrow">
              <BorrowBook />
            </Route>
            {/* URL for the book Creation page */}
            <Route exact path="/books/create">
              <BookCreate />
            </Route>
            {/* URL for book list page */}
            <Route exact path="/books">
              <BookListContainer />
            </Route>
            <Route path="/copies/:id(\d+)/update">
              <CopyUpdate />
            </Route>
            <Route path="/copies/:id(\d+)/delete">
              <CopyDelete />
            </Route>
            <Route path="/books/:id(\d+)/copies/add">
              <CopyCreate />
            </Route>
            <Route path="/books/:id(\d+)/copies">
              <Copies />
            </Route>
            {/* URL for book details page*/}
            <Route path="/books/:id(\d+)">
              <BookDetailsContainer />
            </Route>
            <Route exact path="/signup">
              <Signup />
            </Route>
            <Route exact path="/librarian/signup">
              <LibrarianSignup />
            </Route>
            <Route exact path="/genre">
              <Genres />
            </Route>
            <Route exact path="/genre/:id(\d+)">
              <GenreDetails />
            </Route>
            URL for the deletion page of a specific author
            <Route exact path="/genre/:id(\d+)/delete">
              <GenreDelete />
            </Route>
            URL for the update page of a specific author
            <Route exact path="/genre/:id(\d+)/update">
              <GenreUpdate />
            </Route>
            <Route exact path="/genre/create">
              <GenreCreate />
            </Route>
            <Route exact path="/language">
              <Languages />
            </Route>
            <Route exact path="/language/:id(\d+)">
              <LanguageDetails />
            </Route>
            <Route exact path="/language/create">
              <LanguageCreate />
            </Route>
            <Route exact path="/language/:id(\d+)/update">
              <LanguageUpdate />
            </Route>
            <Route exact path="/language/:id(\d+)/delete">
              <LanguageDelete />
            </Route>
            <Route exact path="/users">
              <Users />
            </Route>
            <Route exact path="/users/:id(\d+)">
              <UserDetails />
            </Route>
            <Route exact path="/users/create">
              <UserCreate />
            </Route>
            <Route exact path="/users/:id(\d+)/update">
              <UserUpdate />
            </Route>
            <Route exact path="/my_borrowed">
              <MyBorrowed />
            </Route>
            <Route exact path="/borrowed/:id(\d+)/return">
              <ReturnBorrowed />
            </Route>
            <Route exact path="/borrowed/:id(\d+)/update">
              <BorrowUpdate />
            </Route>
            <Route>
              <ErrorComponent error={{ status: 404, message: "Not found." }} />
            </Route>
          </Switch>
        </AuthContextProvider>
      </div>
    </Router>
  );
}

export default App;
