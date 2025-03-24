package org.example.laba.services;

import org.example.laba.models.Document;
import org.example.laba.repos.DocumentRepository;
import org.example.laba.utils.exceptions.DocumentCreationException;
import org.example.laba.utils.exceptions.DocumentNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class DocumentService {

    private final DocumentRepository documentRepository;

    @Autowired
    public DocumentService(DocumentRepository documentRepository) {
        this.documentRepository = documentRepository;
    }

    public List<Document> getAllDocuments() {
        return documentRepository.findAll();
    }

    public Document createDocument(Document document) {
        try {
            return documentRepository.save(document);
        } catch (Exception e) {
            throw new DocumentCreationException("Не удалось создать документ");
        }
    }

    public Optional<Document> getDocumentById(Integer id) {
        return documentRepository.findById(id);
    }

    public Document updateDocument(Integer id, Document document) {
        Document existingDocument = documentRepository.findById(id)
                .orElseThrow(() -> new DocumentNotFoundException("Document not found with id: " + id));

        if (document.getTitle() != null) {
            existingDocument.setTitle(document.getTitle());
        }
        if (document.getFileUrl() != null) {
            existingDocument.setFileUrl(document.getFileUrl());
        }
        if (document.getCategory() != null) {
            existingDocument.setCategory(document.getCategory());
        }

        try {
            return documentRepository.save(existingDocument);
        } catch (Exception e) {
            throw new RuntimeException("Error updating document", e);  // Обработка ошибки сохранения
        }
    }

    public void deleteDocument(Integer id) {
        if (!documentRepository.existsById(id)) {
            throw new DocumentNotFoundException("Document not found with id: " + id);
        }
        documentRepository.deleteById(id);
    }
}
