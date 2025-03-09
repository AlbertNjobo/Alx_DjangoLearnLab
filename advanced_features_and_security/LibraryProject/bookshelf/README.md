# Permissions and Groups Setup Guide

## Overview
This Django application implements a permission and group system for managing access to articles.

## Models and Permissions
- `Article` model includes custom permissions:
  - `can_view`: Allows viewing articles
  - `can_create`: Allows creating new articles
  - `can_edit`: Allows editing existing articles
  - `can_delete`: Allows deleting articles

## Groups Configuration
1. Editors:
   - Permissions: `can_create`, `can_edit`
   - Purpose: Can create and edit articles

2. Viewers:
   - Permissions: `can_view`
   - Purpose: Read-only access to articles

3. Admins:
   - Permissions: All (`can_view`, `can_create`, `can_edit`, `can_delete`)
   - Purpose: Full control over articles

## Setup Instructions
1. Create groups in Django Admin:
   - Go to /admin/auth/group/
   - Add groups: 'Editors', 'Viewers', 'Admins'
   - Assign appropriate permissions from the Article model

2. Assign users to groups:
   - Go to /admin/your_app_name/customuser/
   - Edit user and assign to appropriate group

## Usage in Views
- Views are protected with `@permission_required` decorator
- Additional author-based checks for edit and delete operations
- Access attempts without proper permissions raise PermissionDenied

## Testing
1. Create test users in admin
2. Assign them to different groups
3. Attempt to:
   - View articles
   - Create new articles
   - Edit existing articles
   - Delete articles
4. Verify appropriate access control
