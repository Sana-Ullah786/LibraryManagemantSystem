import React, { useEffect, useState, useContext } from 'react';
import { useParams, Link, useRouteMatch } from 'react-router-dom';
import { client } from '../../axios';
import { AuthContext } from '../../contexts/AuthContext';
import { ErrorObject } from '../../CustomTypes';
import ErrorComponent from '../ErrorComponent';

function GenreDetails() {
  const { id }: { id: string } = useParams();
  const genreId: number = parseInt(id); 

  const { url }: { url: string } = useRouteMatch();

  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);

  const [genre, setGenre] = useState<string | null | undefined>('');
  const [error, setError] = useState<ErrorObject>();

  useEffect(() => {
    client
      .GetGenreDetails(genreId) 
      .then((response) => {
        if (response) {
          setGenre(response.genre);
        }
      })
      .catch((error) => {
        setError(error);
      });
  }, [genreId]);

  function librarianLinks() {
    return (
      <>
        <Link to={`${url}/update`} style={{ color: 'orange' }}>
          {' '}
          Update{' '}
        </Link>
        <Link to={`${url}/delete`} style={{ color: 'red' }}>
          Delete
        </Link>
      </>
    );
  }

  if (error != null) {
    return <ErrorComponent error={error} />;
  }

  return (
    <div>
      <h1>Genre: {genre}</h1>
      {isLibrarian === true ? librarianLinks() : null}
      {/* Placeholder for genre details */}
    </div>
  );
}

export default GenreDetails;
