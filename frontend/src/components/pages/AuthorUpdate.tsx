import React, { 
    ReactElement,
    useEffect,
    useState,
    useContext,
} from 'react'
import {client} from '../../axios'
import {
    useParams,
} from 'react-router-dom'
import AuthorForm from '../AuthorForm';
import {SubmitHandler} from 'react-hook-form'
import {useHistory} from 'react-router-dom'
import {
    AuthorDetails,
    ErrorObject,
} from '../../CustomTypes'
import ErrorComponent from '../ErrorComponent'
import {AuthContext} from '../../contexts/AuthContext'

interface Props {
    
}

function AuthorUpdate(props: Props): ReactElement {
    let {id}:{id: string} = useParams();
    const history = useHistory()

    const [firstName,setFirstName] = useState<string|null|undefined>()
    const [lastName,setLastName] = useState<string|null|undefined>()
    const [dateOfBirth,setDateOfBirth] = useState<string|null|undefined>()
    const [dateOfDeath,setDateOfDeath] = useState<string|null|undefined>()
    const [loaded,setLoaded] = useState<boolean>(false)
    const [error,setError] = useState<ErrorObject>()
    const {isLibrarian}: {isLibrarian: boolean} = useContext(AuthContext)
    const {isAuthenticated}: {isAuthenticated: boolean} = useContext(AuthContext)

    /**
     * When the page loads, we will use the API to get the current values of the author object we are updating.
     * This data will be used to prefill the form, which will render after the data has been obtained
     */
    useEffect(() => {
        client.GetAuthorDetails(id)
        .then(Author=>{
            if (Author){
                setFirstName(Author.first_name)
                setLastName(Author.last_name)
                setDateOfBirth(Author.date_of_birth)
                setDateOfDeath(Author.date_of_death)
                setLoaded(true)
            }
        })
        .catch(error=>{
            setError(error)
        })
        .catch(error=>{
            setError(error)
        })
    },[id])

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

    /**
     * The onSubmit function takes an AuthorDetails object as an argument and uses it to make a post request to 
     * update the desires author
     * @param data The AuthorDetails interface is defined in the AuthorForm component
     */
    const onSubmit: SubmitHandler<AuthorDetails> = data => {
        client.PutAuthor(id,cleanData(data))
        .then(response =>{
            history.push('/authors/'+id)
        })
    }

    //We must clean the data to make sure empty strings are replaced with null values to make the put request valid
    function cleanData(data:AuthorDetails){
        data.first_name = data.first_name===""? null: data.first_name
        data.last_name = data.last_name===""? null: data.last_name
        data.date_of_birth = data.date_of_birth===""? null: data.date_of_birth
        data.date_of_death = data.date_of_death===""? null: data.date_of_death
        return data
    }

    if (error != null){
        return (
            <ErrorComponent error={error} />
        )
    }


    return (
        <div>
            {/* The loaded state allows us to only render the form when the data has been obtained, 
            This will allow us to prefill the form with the author data when it renders */}
            {loaded === true?
            <AuthorForm
                first_name={firstName}
                last_name={lastName}
                date_of_birth={dateOfBirth}
                date_of_death={dateOfDeath}
                onSubmit = {onSubmit}
            />
            :<h1>--Loading--</h1>}

        </div>
    )
}

export default AuthorUpdate
