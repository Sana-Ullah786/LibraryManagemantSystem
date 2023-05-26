import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { client } from "../../axios";
import { UserDetails as User, ErrorObject } from "../../CustomTypes";
import ErrorComponent from "../ErrorComponent";
import { BorrowedList } from "../BorrowedList";
import { BorrowedIn } from "../../CustomTypes";
import { Pagination } from "./pagination";

function UserDetails() {
  let { id }: { id: string } = useParams();
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<ErrorObject | null>(null);
  const [borrowedList, setBorrowedList] = useState<BorrowedIn[]>([]);
  const [page, setPage] = useState<number>(1);

  useEffect(() => {
    client
      .GetUserDetails(id)
      .then((userData) => {
        setUser(userData);
      })
      .catch((error) => {
        setError(error);
      });
    client
      .GetBorrowedForUser(id, page)
      .then((borrowed) => {
        setBorrowedList(borrowed);
      })
      .catch((error) => {
        setError(error);
      });
  }, [id]);

  if (error) {
    return <ErrorComponent error={error} />;
  }

  if (!user) {
    return <h1>Loading...</h1>;
  }

  return (
    <div className="background-image">
      <div className="modal">
        <div className="inner-modal">
          <h1>User Details</h1>
          <p>Email: {user.email}</p>
          <p>Username: {user.username}</p>
          <p>First Name: {user.first_name}</p>
          <p>Last Name: {user.last_name}</p>
          <p>Contact Number: {user.contact_number}</p>
          <p>Address: {user.address}</p>
        </div>
        <h2>Books borrowed by this user:</h2>
        <BorrowedList borrowedList={borrowedList} />
        <Pagination
          page={page}
          setPage={setPage}
          showNext={borrowedList.length === 10}
        />
      </div>
    </div>
  );
}

export default UserDetails;
