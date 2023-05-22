import React, { useEffect, useState, useContext } from 'react';
import { useParams, Link, useRouteMatch } from 'react-router-dom';
import { client } from '../../axios';
import { AuthContext } from '../../contexts/AuthContext';
import { ErrorObject } from '../../CustomTypes';
import ErrorComponent from '../ErrorComponent';
import "../style.css"; // Import the Languages CSS file

function LanguageDetails() {
  // Getting the id of the language from the URL of the current page as a parameter
  let {id}:{id: string} = useParams();
  const { url } = useRouteMatch();

  const { isLibrarian } = useContext(AuthContext);

  const [language, setLanguage] = useState<string | null | undefined>('');
  const [error, setError] = useState<ErrorObject>();

  // Getting the details of a specific language from the API endpoint
  useEffect(() => {
    client.GetLanguageDetails(id)
      .then(
        (response) => {
          if (response) {
            setLanguage(response.language);
          }
        },
        (error) => {
          setError(error);
        }
      )
      .catch((error) => {
        setError(error);
      });
  }, [id]);

  // This creates links to the update and delete librarian pages
  function librarianLinks() {
    return (
      <>
        <Link to={`${url}/update`} className="genre-list-update-button">
          Update
        </Link>
        <Link to={`${url}/delete`}className="genre-list-delete-button">
          Delete
        </Link>
      </>
    );
  }

  // Rendering out the Language page
  if (error) {
    return <ErrorComponent error={error} />;
  }

  return (
    <div className='background-image'>
      <h1>Language: {language}</h1>
      {isLibrarian === true ? librarianLinks() : null}
      <div>
        <h3>Books</h3>
        <ul>
          <li style={{ fontWeight: 'bold' }}>Placeholder for book title</li>
          <p>Book description</p>
        </ul>
      </div>
    </div>
  );
}

export default LanguageDetails;
