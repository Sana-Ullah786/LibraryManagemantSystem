import React, { ReactElement, useEffect, useState, useContext } from "react";
import { client } from "../../axios";
import { useParams, useHistory } from "react-router-dom";
import UserForm from "./UserForm";
import { SubmitHandler } from "react-hook-form";
import { ErrorObject, UserDetails } from "../../CustomTypes";
import ErrorComponent from "../ErrorComponent";
import { AuthContext } from "../../contexts/AuthContext";

interface Props {}

function UserUpdateMe(props: Props): ReactElement {
  const history = useHistory();

  const [user, setUser] = useState<UserDetails | null>(null);
  const [loaded, setLoaded] = useState<boolean>(false);
  const [error, setError] = useState<ErrorObject>();
  const {
    isLibrarian,
    isAuthenticated,
  }: { isLibrarian: boolean; isAuthenticated: boolean } =
    useContext(AuthContext);

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) {
      setUser(JSON.parse(user));
      setLoaded(true);
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated === true) {
      if (isLibrarian !== true) {
        let err: ErrorObject = {
          status: 403,
          message: "Forbidden. You do not have permission to view this page",
        };
        setError(err);
      }
    } else {
      let err: ErrorObject = {
        status: 401,
        message: "Unauthorized, you must be logged in to view this page",
      };
      setError(err);
    }
  }, [isAuthenticated, isLibrarian]);

  const onSubmit: SubmitHandler<UserDetails> = (data) => {
    client
      .UpdateMe(data)
      .then((response) => {
        alert("Details updated successfully!");
      })
      .catch((error) => alert(error));
  };

  return (
    <div className="background-image">
      {loaded ? (
        <UserForm user={user} onSubmit={onSubmit} />
      ) : (
        <h1>--Loading--</h1>
      )}
    </div>
  );
}

export default UserUpdateMe;
