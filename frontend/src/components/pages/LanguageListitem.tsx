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
    <div className="language-list-item">
      <span className="language-name">{item.language}</span>
      <div className="language-actions">
        <Link to={linksto} className="language-action-button">Update</Link>
        <Link to={linksto} className="language-action-button">Delete</Link>
      </div>
    </div>
  );
};

export default LanguageListItem;
