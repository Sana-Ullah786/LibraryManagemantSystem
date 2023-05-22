import React, { ReactElement, useEffect, useState, useContext } from 'react';
import { client } from '../../axios';
import { useParams, useHistory } from 'react-router-dom';
import GenreForm from './GenreForm';
import { SubmitHandler } from 'react-hook-form';
import { ErrorObject, GenreDetails } from '../../CustomTypes';
import ErrorComponent from '../ErrorComponent';
import { AuthContext } from '../../contexts/AuthContext';

interface Props {}

function GenreUpdate(props: Props): ReactElement {
  const { id }: { id: string } = useParams();
  const genreId: number = parseInt(id); // Parse id as a number
  const history = useHistory();

  const [genre, setGenre] = useState<string | null | undefined>();
  const [loaded, setLoaded] = useState<boolean>(false);
  const [error, setError] = useState<ErrorObject>();
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  const { isAuthenticated }: { isAuthenticated: boolean } = useContext(AuthContext);

  useEffect(() => {
    client
      .GetGenreDetails(genreId)
      .then((genreData) => {
        if (genreData) {
          setGenre(genreData.genre);
          setLoaded(true);
        }
      })
      .catch((error) => {
        setError(error);
      });
  }, [genreId]);

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

  const onSubmit: SubmitHandler<GenreDetails> = (data) => {
    client
      .PutGenre(cleanData(data), genreId) 
      .then((response) => {
        history.push('/genre/' + genreId); 
      });
  };

  function cleanData(data: GenreDetails) {
    data.genre = data.genre !== null ? data.genre : '';

 
    return data;
  }

  if (error != null) {
    return <ErrorComponent error={error} />;
  }

  return (
    <div>
      {loaded === true ? (
        <GenreForm genre={genre || ''} onSubmit={onSubmit} />
      ) : (
        <h1>--Loading--</h1>
      )}
    </div>
  );
}

export default GenreUpdate;
