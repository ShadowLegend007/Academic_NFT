module AcademicNFT::AcademicNFT {
    use std::error;
    use std::signer;
    use std::string::{Self, String};
    use std::vector;
    use aptos_framework::account;
    use aptos_framework::event::{Self, EventHandle};
    use aptos_framework::timestamp;
    use aptos_token::token::{Self, TokenDataId};
    
    // Errors
    const ENOT_AUTHORIZED: u64 = 1;
    const EACADEMIC_NFT_ALREADY_EXISTS: u64 = 2;
    const EACADEMIC_NFT_DOES_NOT_EXIST: u64 = 3;
    
    // Token collection name
    const COLLECTION_NAME: vector<u8> = b"Academic NFT Collection";
    const COLLECTION_DESCRIPTION: vector<u8> = b"Collection of academic papers verified for originality";
    const COLLECTION_URI: vector<u8> = b"https://academic-nft.example.com/collection";
    
    // NFT properties
    struct AcademicNFTData has store, drop {
        title: String,
        summary: String,
        plagiarism_score: u64,  // Score as percentage (0-100)
        ipfs_cid: String,
        timestamp: u64,
        wallet_address: address,
        feedback_cid: String,   // Optional feedback from teacher
    }
    
    // Events
    struct MintAcademicNFTEvent has drop, store {
        token_id: TokenDataId,
        title: String,
        plagiarism_score: u64,
        ipfs_cid: String,
        timestamp: u64,
        wallet_address: address,
    }
    
    struct UpdateFeedbackEvent has drop, store {
        token_id: TokenDataId,
        feedback_cid: String,
        teacher_address: address,
    }
    
    // Resource to store NFT collection info and events
    struct AcademicNFTCollection has key {
        token_data_id: TokenDataId,
        mint_events: EventHandle<MintAcademicNFTEvent>,
        feedback_events: EventHandle<UpdateFeedbackEvent>,
    }
    
    // Initialize the collection
    public entry fun initialize_collection(account: &signer) {
        let account_addr = signer::address_of(account);
        
        // Create the collection
        let collection_name = string::utf8(COLLECTION_NAME);
        let description = string::utf8(COLLECTION_DESCRIPTION);
        let collection_uri = string::utf8(COLLECTION_URI);
        let maximum_supply = 0; // Unlimited supply
        let mutate_setting = vector::empty<bool>();
        
        token::create_collection(
            account,
            collection_name,
            description,
            collection_uri,
            maximum_supply,
            mutate_setting
        );
    }
    
    // Mint a new academic NFT
    public entry fun mint(
        account: &signer,
        title: String,
        summary: String,
        plagiarism_score: u64,
        ipfs_cid: String,
        timestamp: u64,
        wallet_address: address
    ) acquires AcademicNFTCollection {
        let account_addr = signer::address_of(account);
        
        // Only the wallet owner can mint their own NFT
        assert!(account_addr == wallet_address, error::permission_denied(ENOT_AUTHORIZED));
        
        // Initialize collection if it doesn't exist
        if (!exists<AcademicNFTCollection>(account_addr)) {
            initialize_collection(account);
            
            // Create the resource to track the collection
            let collection_name = string::utf8(COLLECTION_NAME);
            let token_name = title;
            let token_uri = string::utf8(b"https://ipfs.io/ipfs/");
            let token_uri = string::append(token_uri, ipfs_cid);
            
            // Create token data id
            let token_data_id = token::create_tokendata(
                account,
                collection_name,
                token_name,
                summary,
                1, // Maximum supply of 1 for this NFT
                token_uri,
                account_addr, // Royalty payee address
                0, // Royalty points denominator
                0, // Royalty points numerator
                token::create_token_mutability_config(
                    &vector<bool>[false, false, false, false, true]
                ),
                vector::empty<String>(), // Property keys
                vector::empty<vector<u8>>(), // Property values
                vector::empty<String>() // Property types
            );
            
            move_to(account, AcademicNFTCollection {
                token_data_id,
                mint_events: account::new_event_handle<MintAcademicNFTEvent>(account),
                feedback_events: account::new_event_handle<UpdateFeedbackEvent>(account),
            });
        };
        
        let academic_nft_collection = borrow_global_mut<AcademicNFTCollection>(account_addr);
        
        // Mint the token
        let token_id = token::mint_token(
            account,
            academic_nft_collection.token_data_id,
            1 // Amount to mint (always 1 for NFTs)
        );
        
        // Store NFT data
        let nft_data = AcademicNFTData {
            title,
            summary,
            plagiarism_score,
            ipfs_cid,
            timestamp,
            wallet_address,
            feedback_cid: string::utf8(b""), // Empty feedback initially
        };
        
        // Emit mint event
        event::emit_event<MintAcademicNFTEvent>(
            &mut academic_nft_collection.mint_events,
            MintAcademicNFTEvent {
                token_id: academic_nft_collection.token_data_id,
                title,
                plagiarism_score,
                ipfs_cid,
                timestamp,
                wallet_address,
            }
        );
    }
    
    // Add teacher feedback to an NFT
    public entry fun add_feedback(
        teacher: &signer,
        student_address: address,
        feedback_cid: String
    ) acquires AcademicNFTCollection {
        // Verify the student has an NFT collection
        assert!(exists<AcademicNFTCollection>(student_address), error::not_found(EACADEMIC_NFT_DOES_NOT_EXIST));
        
        let academic_nft_collection = borrow_global_mut<AcademicNFTCollection>(student_address);
        let teacher_address = signer::address_of(teacher);
        
        // Emit feedback event
        event::emit_event<UpdateFeedbackEvent>(
            &mut academic_nft_collection.feedback_events,
            UpdateFeedbackEvent {
                token_id: academic_nft_collection.token_data_id,
                feedback_cid,
                teacher_address,
            }
        );
    }
}