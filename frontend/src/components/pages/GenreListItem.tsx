import React, { useContext } from 'react';
import { Link, useRouteMatch } from 'react-router-dom';
import { AuthContext } from '../../contexts/AuthContext';
import { Genre } from '../../CustomTypes';
import '../style.css'; // Import the Genres CSS file

export type GenreListItemProps = {
  key: number;
  item: Genre;
  linksto: string;
};

function GenreListItem(props: GenreListItemProps) {
  const { url }: { url: string } = useRouteMatch();
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);

  function librarianLinks() {
    return (
      <>
        <div className="genre-list-item-buttons">
          <Link to={`${url}/${props.item.id}/update`} className="genre-list-update-button">Update</Link>
          <Link to={`${url}/${props.item.id}/delete`} className="genre-list-delete-button">Delete</Link>
        </div>

      </>
    );
  }

  return (
    <>
      <Link to={props.linksto}>
        {props.item.genre}
      </Link>
      {isLibrarian === true ? librarianLinks() : null}
    </>
  );
}

export default GenreListItem;
