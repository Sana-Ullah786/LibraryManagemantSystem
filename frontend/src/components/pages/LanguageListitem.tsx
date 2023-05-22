import React from 'react';
import { Link } from 'react-router-dom';
import { Language } from '../../CustomTypes';
import "../style.css"; // Import the Languages CSS file

interface LanguageListItemProps {
  item: Language;
  linksto: string;
}

const LanguageListItem: React.FC<LanguageListItemProps> = ({ item, linksto }) => {
  return (
    <div  className="genre-list-item">
      <span className="language-name">
      <Link to={linksto} > {item.language}</Link>
      </span>

      <div >
        <Link to={`language/${item.id}/update`} className="genre-list-update-button">Update</Link>
        <Link to={`language/${item.id}/delete`} className="genre-list-delete-button">Delete</Link>
      </div>
    </div>
  );
};

export default LanguageListItem;
