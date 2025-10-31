// Main JavaScript file for Land Records Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // File input custom styling
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            const nextSibling = e.target.nextElementSibling;
            
            if (fileName) {
                if (nextSibling && nextSibling.classList.contains('custom-file-label')) {
                    nextSibling.textContent = fileName;
                }
                // Show file name near the input
                const fileNameDisplay = document.createElement('div');
                fileNameDisplay.className = 'selected-file-name mt-2 text-primary';
                fileNameDisplay.innerHTML = `<i class="fas fa-file me-1"></i> ${fileName}`;
                
                // Remove any existing filename display before adding new one
                const existingFileNameDisplay = e.target.parentNode.querySelector('.selected-file-name');
                if (existingFileNameDisplay) {
                    existingFileNameDisplay.remove();
                }
                
                e.target.parentNode.appendChild(fileNameDisplay);
            }
        });
    });
    
    // Confirmation dialog for delete actions
    const deleteButtons = document.querySelectorAll('a[href*="delete"]');
    deleteButtons.forEach(button => {
        if (!button.hasAttribute('data-bs-toggle')) {  // Skip if it's already using a modal
            button.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this record? This action cannot be undone.')) {
                    e.preventDefault();
                }
            });
        }
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });
    
    // Preview uploaded image files before submission
    const documentInput = document.querySelector('input[name="document"]');
    if (documentInput) {
        documentInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Check if it's an image file
                if (file.type.match('image.*')) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        // Create or update image preview
                        let previewContainer = document.getElementById('document-preview-container');
                        if (!previewContainer) {
                            previewContainer = document.createElement('div');
                            previewContainer.id = 'document-preview-container';
                            previewContainer.className = 'mt-3 p-2 border rounded text-center';
                            documentInput.parentNode.appendChild(previewContainer);
                        }
                        
                        previewContainer.innerHTML = `
                            <h6 class="mb-2">Preview:</h6>
                            <img src="${e.target.result}" class="img-fluid img-thumbnail" style="max-height: 200px;" alt="Document Preview">
                        `;
                    }
                    reader.readAsDataURL(file);
                }
            }
        });
    }
    
    // Search form highlight matches
    const searchForm = document.querySelector('form[method="GET"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="search"]');
        const searchValue = searchInput?.value;
        
        if (searchValue) {
            // Highlight search term in record titles and descriptions
            const highlightText = (element, term) => {
                if (!element || !term) return;
                
                const innerHTML = element.innerHTML;
                const index = innerHTML.toLowerCase().indexOf(term.toLowerCase());
                if (index >= 0) {
                    element.innerHTML = innerHTML.substring(0, index) + 
                        `<span class="bg-warning text-dark">${innerHTML.substring(index, index + term.length)}</span>` + 
                        innerHTML.substring(index + term.length);
                }
            };
            
            // Apply highlighting to table cells
            document.querySelectorAll('table td:first-child a').forEach(el => {
                highlightText(el, searchValue);
            });
            
            document.querySelectorAll('table td:nth-child(2)').forEach(el => {
                highlightText(el, searchValue);
            });
        }
    }
});
