import { ReactElement, useEffect, useState, useContext } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import { client } from '../../axios';
import { ErrorObject } from '../../CustomTypes';
import ErrorComponent from '../ErrorComponent';
import { AuthContext } from '../../contexts/AuthContext';
import '../style.css'; // Import the Genres CSS file
interface Props {}

function GenreDelete(props: Props): ReactElement {
  const { id }: { id: string } = useParams();
  const history = useHistory();
  const [genre, setGenre] = useState<string | null | undefined>('--Loading--');
  const [error, setError] = useState<ErrorObject>();
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  const { isAuthenticated }: { isAuthenticated: boolean } = useContext(AuthContext);
  const genreId: number = parseInt(id);

  useEffect(() => {
    client
      .GetGenreDetails(genreId)
      .then((genreData) => {
        setGenre(genreData.genre);
      })
      .catch((error) => {
        setError(error);
      });
  }, [id]);

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

  function handleDelete() {
    client
      .DeleteGenre(id)
      .then((response) => {
        history.push('/genre');
      });
  }

  if (error != null) {
    return <ErrorComponent error={error} />;
  }

  return (
    <div className='background-image'>
      <h1>Delete Genre: {genre}</h1>
      <button onClick={handleDelete} className='genre-list-danger-button'> Yes, Delete</button>
    </div>
  );
}

export default GenreDelete;
