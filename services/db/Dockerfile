FROM postgres:15-alpine

# Copy initialization script
COPY init_complete.sql /docker-entrypoint-initdb.d/

# Set environment variables
ENV POSTGRES_DB=bhiv_hr
ENV POSTGRES_USER=bhiv_user

# Expose port
EXPOSE 5432