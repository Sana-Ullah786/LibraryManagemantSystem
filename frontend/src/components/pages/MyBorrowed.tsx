import React, { useEffect, useState, useContext } from "react";
import { BorrowedIn, ErrorObject } from "../../CustomTypes";
import { useParams } from "react-router";
import { client } from "../../axios";
import { AuthContext } from "../../contexts/AuthContext";
import { useRouteMatch, Link } from "react-router-dom";
import ErrorComponent from "../ErrorComponent";
import { BorrowedList } from "../BorrowedList";
import ScrollView from "../Scrollview";
import { Pagination } from "./pagination";

const MyBorrowed = (props: { showLinks?: boolean }) => {
  /*
   * BookDetailsContainer performs all the computation and api calls to fetch book details.
   * It delegates the task of actually displaying the data to BookDetailsPresentation.
   */

  //id is extracted from url
  let { id }: { id: string } = useParams();

  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  let { url }: { url: string } = useRouteMatch(); // The url of this page

  // book, genre and language are intentially allowed to be undefined. We display the page once these values are loaded

  let [myBorrowed, setMyBorrowed] = useState<BorrowedIn[]>([]); //The myBorrowed to be displayed

  const [error, setError] = useState<ErrorObject>();

  const [page, setPage] = useState<number>(1);

  useEffect(() => {
    // Getting value of book from the api
    client
      .GetMyBorrowed(page)
      .then(
        (newMyBorrowed: BorrowedIn[]) => {
          newMyBorrowed.sort((a, b) => (a.id > b.id ? 1 : -1));
          setMyBorrowed(newMyBorrowed);
        }
        //(error) => { console.log(`Error! The book with id ${id} does not exist.`); }
      )
      .catch((err) => {
        setError(err);
      });
  }, [id]);

  console.log(myBorrowed);

  // The book details are presented once all details have been received
  return (
    <div className="background-image">
      <div className="modal">
        <h1>My Borrowed Books</h1>
        <ScrollView>
          <BorrowedList borrowedList={myBorrowed} />
        </ScrollView>
        <Pagination
          page={page}
          setPage={setPage}
          showNext={myBorrowed.length === 10}
        />
      </div>
    </div>
  );
};

// By default links are always shown if the user is a librarian
MyBorrowed.defaultProps = { showLinks: true };

export default MyBorrowed;
