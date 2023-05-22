import React, { ReactElement, useContext, useEffect, useState } from "react";
import AuthorForm from "../AuthorForm";
import { SubmitHandler } from "react-hook-form";
import { client } from "../../axios";
import { useHistory } from "react-router-dom";
import { AuthorDetails } from "../../CustomTypes";
import { AuthContext } from "../../contexts/AuthContext";
import { ErrorObject } from "../../CustomTypes";
import ErrorComponent from "../ErrorComponent";

interface Props {}
function AuthorCreate(props: Props): ReactElement {
  const history = useHistory();
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  const { isAuthenticated }: { isAuthenticated: boolean } =
    useContext(AuthContext);
  const [error, setError] = useState<ErrorObject>();

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

  /**
   * We define our onSubmit function and use it to make a post request to the correct API endpoint,
   * @param data AuthorDetails is defined in the AuthorForms component page,
   */
  const onSubmit: SubmitHandler<AuthorDetails> = (data) => {
    client.PostAuthor(cleanData(data)).then((AuthorID) => {
      history.push("/authors/" + AuthorID);
    });
  };

  //We must clean our data to ensure empty strings are sent as null values for the POST request to be valid
  function cleanData(data: AuthorDetails) {
    data.first_name = data.first_name === "" ? null : data.first_name;
    data.last_name = data.last_name === "" ? null : data.last_name;
    data.birth_date = data.birth_date === "" ? null : data.birth_date;
    data.death_date = data.death_date === "" ? null : data.death_date;
    return data;
  }

  if (error) {
    return <ErrorComponent error={error} />;
  }

  return (
    <div>
      {/* We senf the onSubmit function as a prop to the AuthorForm component */}
      <AuthorForm onSubmit={onSubmit} />
    </div>
  );
}

export default AuthorCreate;
