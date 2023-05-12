import React, { 
    ReactElement,
    useEffect,
    useState,
    useContext,
} from 'react';
import {
    useParams,
    useHistory,
} from 'react-router-dom';
import {client} from '../../axios'
import {ErrorObject} from '../../CustomTypes'
import ErrorComponent from '../ErrorComponent'
import {AuthContext} from '../../contexts/AuthContext'

interface Props {

}

function AuthorDelete(props: Props): ReactElement {
    let {id}:{id: string} = useParams();
    const history = useHistory()
    const [firstName,setFirstName] = useState<string|null|undefined>("--Loading--")
    const [lastName,setLastName] = useState<string|null|undefined>("--Loading--")
    const [error,setError] = useState<ErrorObject>()
    const {isLibrarian}: {isLibrarian: boolean} = useContext(AuthContext)
    const {isAuthenticated}: {isAuthenticated: boolean} = useContext(AuthContext)

    //We will make a get request to obtain the details of the author we are about to delete.
    useEffect(() =>{
        client.GetAuthorDetails(id)
        .then(Author=>{
            setFirstName(Author.first_name)
            setLastName(Author.last_name)
        })
        .catch(
            error=>{
                setError(error)
            }
        )
    }
    ,[id])

    useEffect(()=>{
        if (isAuthenticated === true){
            if (isLibrarian !== true){
                let err:ErrorObject = {
                    status:403,
                    message:"Forbidden. You do not have permission to view this page"
                }
                setError(err)
            }
        }
        else{
            let err:ErrorObject = {
                status:401,
                message:"Unauthorized, you must be logged in to view this page"
            }
            setError(err)
        }
    },[isAuthenticated,isLibrarian])

    //Deleting the author and then redirecting to the /authors page upon success
    function handleClick()
    {
        client.DeleteAuthor(id)
        .then(
            (response) => {
                history.push('/authors')
            }    
        )
    }
    if (error != null){
        return (
            <ErrorComponent error={error} />
        )
    }
    
    return (
        <div>
            <h1>DELETE Author {lastName}, {firstName}  ?</h1>
            <button onClick = {handleClick}>Yes, Delete</button>
        </div>
    )
}

export default AuthorDelete
