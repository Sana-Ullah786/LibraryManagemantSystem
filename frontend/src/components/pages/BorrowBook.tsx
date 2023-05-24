import { useHistory } from "react-router-dom";
import { ReactElement, useEffect, useState, useContext } from "react";
import { client } from "../../axios";
import { CopyIn, BorrowedOut } from "../../CustomTypes";
import BookForm from "../BookForm";
import BorrowForm from "../BorrowForm";
import { useParams } from "react-router-dom";
import { AuthContext } from "../../contexts/AuthContext";

function BorrowBook(): ReactElement {
  const history = useHistory();

  let { id }: { id: string } = useParams();
  const {
    user_id,
    username,
    isLibrarian,
  }: { user_id: number; username: string; isLibrarian: boolean } =
    useContext(AuthContext);

  let [copy, setCopy]: [
    CopyIn | undefined,
    React.Dispatch<React.SetStateAction<CopyIn | undefined>>
  ] = useState();

  useEffect(() => {
    // Getting value of book from the api
    client
      .GetCopiesofBook(id)
      .then(
        (newCopies: CopyIn[]) => {
          newCopies.forEach((newCopy: CopyIn) => {
            if (newCopy.status.status === "available") {
              setCopy(newCopy);
            }
          });
        }
        //(error) => { console.log(`Error! The book with id ${id} does not exist.`); }
      )
      .catch((err) => {
        alert(err);
      });
  }, [id]);

  function submitHandler(borrowed: BorrowedOut) {
    client
      .CreateBorrowed(borrowed)
      .then((borrowedId) => {
        history.push("/my_borrowed");
      })
      .catch((error) => {
        alert(error);
      });
  }

  function getCurrentDateTime() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");

    return `${year}-${month}-${day}T${hours}:${minutes}`;
  }

  return (
    <div className="background-image">
      {copy !== undefined && (
        <BorrowForm
          borrowed={{
            id: -1,
            copy: copy,
            user: {
              id: user_id,
              username: username,
              email: "",
              password: "",
              first_name: "",
              last_name: "",
              address: "",
              contact_number: "",
            },
            issueDate: getCurrentDateTime(),
            dueDate: "",
            returnDate: null,
          }}
          isLibrarian={isLibrarian}
          submitHandler={submitHandler}
        />
      )}
    </div>
  );
}

export default BorrowBook;
