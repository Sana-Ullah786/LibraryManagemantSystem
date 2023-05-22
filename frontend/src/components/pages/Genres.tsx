import React, { useEffect, useState, useContext } from 'react';
import { client } from '../../axios';
import GenreListItem from './GenreListItem';
import { Link, useRouteMatch } from 'react-router-dom';
import { AuthContext } from '../../contexts/AuthContext';
import { Genre, ErrorObject } from '../../CustomTypes';
import ErrorComponent from '../ErrorComponent';
import '../style.css'; // Import the Genres CSS file

function Genres() {
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);

  let { url }: { url: string } = useRouteMatch();

  const [genreList, setGenreList] = useState<Genre[]>([]);
  const [error, setError] = useState<ErrorObject>();

  useEffect(() => {
    client.GetAllGenres()
      .then((genreList) => {
        if (genreList) {
          setGenreList(genreList);
        }
      })
      .catch((error) => {
        setError(error);
      });
  }, []);

  function setGenreListItemComponent(genreList: Genre[]) {
    const genreListItemComponent: JSX.Element[] = genreList.map((genre) => (
      <li className="genre-list-item" key={genre.id}>
        <GenreListItem key={genre.id} item={genre} linksto={`${url}/${genre.id}`} />
      </li>

    ));
    return genreListItemComponent;
  }

  function createGenreLink() {
    return (
      <Link to={`${url}/create`} className="genre-link">
        Create Genre
      </Link>
    );
  }

  if (error != null) {
    return (
      <ErrorComponent error={error} />
    );
  }

  return (
    <div>
      <h1>Genre List</h1>
      <ul className="genre-list">
        {setGenreListItemComponent(genreList)}
      </ul>
      {isLibrarian ? createGenreLink() : null}
    </div>
  );
}

export default Genres;
