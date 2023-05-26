import React, { ReactElement, useContext, useEffect, useState } from 'react';
import GenreForm from './GenreForm';
import { SubmitHandler } from 'react-hook-form';
import { client } from '../../axios';
import { useHistory } from 'react-router-dom';
import { Genre } from '../../CustomTypes';
import { AuthContext } from '../../contexts/AuthContext';
import { ErrorObject } from '../../CustomTypes';
import ErrorComponent from '../ErrorComponent';
import '../style.css'; // Import the Genres CSS file

interface Props {}

function GenreCreate(props: Props): ReactElement {
  const history = useHistory();
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  const { isAuthenticated }: { isAuthenticated: boolean } = useContext(AuthContext);
  const [error, setError] = useState<ErrorObject>();

  useEffect(() => {
    if (isAuthenticated === true) {
      if (isLibrarian !== true) {
        let err: ErrorObject = {
          status: 403,
          message: 'Forbidden. You do not have permission to view this page',
        };
        setError(err);
      }
    } else {
      let err: ErrorObject = {
        status: 401,
        message: 'Unauthorized, you must be logged in to view this page',
      };
      setError(err);
    }
  }, [isAuthenticated, isLibrarian]);

  const onSubmit: SubmitHandler<Genre> = (data) => {
    client.PostGenre(cleanData(data))
    .then((GenreID) => {
      history.push('/genre/' + GenreID);
    })
    .catch((error) => {
        // Handle error and show an error message
        if (error.response && error.response.data && error.response.data.detail) {
          const errorMessage = error.response.data.detail[0].msg;
          // Show the error message to the user (e.g., set it to a state variable to display in the UI)
          setError(errorMessage)
        }});
  };

  function cleanData(data: Genre) {
    const cleanedData = {
      ...data,
      genre: data.genre.trim(),
    };
    return cleanedData;
  }

  if (error) {
    return <ErrorComponent error={error} />;
  }

  return (

    <div className='background-image'>
    <div className='modal'>
        <h1>
        Create Genre
        </h1>
        <p>{Error}</p>
      <GenreForm genre="" onSubmit={onSubmit} /> {/* Pass empty string as the genre prop */}
    </div>
    </div>
  );
}

export default GenreCreate;
